# import csv
import requests
from typing import List, Dict
from requests.exceptions import RequestException, JSONDecodeError
import abc

class StepikAPIClient(abc.ABC):
    """Базовый класс для работы с Stepik API."""
    API_HOST = 'https://stepik.org'

    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})

    def _fetch_object(self, obj_class: str, obj_id: int) -> Dict:
        """Получить один объект по ID."""
        url = f'{self.API_HOST}/api/{obj_class}s/{obj_id}'
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()[f'{obj_class}s'][0]
        except (RequestException, JSONDecodeError) as e:
            print(f"Error fetching {obj_class}: {e}")
            return []

    def _fetch_objects(self, obj_class: str, obj_ids: List[int]) -> List[Dict]:
        """Получить несколько объектов по списку ID."""
        objects = []
        step_size = 30

        for i in range(0, len(obj_ids), step_size):
            chunk = obj_ids[i:i + step_size]
            url = (
                f'{self.API_HOST}/api/{obj_class}s'
                f'?ids[]={"&ids[]=".join(map(str, chunk))}'
            )
            try:
                response = self.session.get(url)
                response.raise_for_status()
                objects.extend(response.json()[f'{obj_class}s'])
            except (RequestException, JSONDecodeError) as e:
                print(f"Error fetching {obj_class}s: {e}")
                return []

        return objects


class CourseData(StepikAPIClient):
    """Класс для экспорта данных курса."""
    def __init__(self, token: str, course_id: int):
        super().__init__(token)
        self.course_id = course_id
        self._data = None
        self._sections = None
        self._lessons = None
        self._steps = None

    @property
    def data(self) -> List[Dict]:
        """Получить данные курса"""
        if self._data is None:
            self._load_course_data()
        return {
            'course': self._data,
            'sections': self._sections,
            'lessons': self._lessons,
            'steps': self._steps
        }

    def _load_course_data(self) -> None:
        course = self._fetch_object('course', self.course_id)
        sections = self._fetch_objects('section', course['sections'])
        units = self._fetch_units(sections)
        #  Словарь из пар {unit_id: lesson_id} для их быстрого сопоставления
        units_dict = {unit['id']: unit['lesson'] for unit in units}
        lessons = self._fetch_lessons(units)
        steps = self._fetch_steps(lessons)

        self._data = self._process_course(course)
        self._data.update({'sections': [section['id'] for section in sections]})

        self._sections = {
            int(section['id']): self._process_section(section, units_dict)
            for section in sections
        }

        self._lessons = {
            lesson['id']: self._process_lesson(lesson) for lesson in lessons
        }

        self._steps = {
            step['id']: self._process_step(step) for step in steps
        }

    def _fetch_units(self, sections: List[Dict]) -> List[Dict]:
        """Получаем данные юнитов"""
        unit_ids = [unit for section in sections for unit in section['units']]
        return self._fetch_objects('unit', unit_ids)

    def _fetch_lessons(self, units: List[Dict]) -> List[Dict]:
        """Получаем данные уроков"""
        lesson_ids = [u['lesson'] for u in units]
        return self._fetch_objects('lesson', lesson_ids)

    def _fetch_steps(self, lessons: List[Dict]) -> List[Dict]:
        """Получаем данные шагов"""
        step_ids = [step for lesson in lessons for step in lesson['steps']]
        return self._fetch_objects('step', step_ids)

    @staticmethod
    def _process_course(course: Dict) -> Dict:
        keys = ['id', 'title']
        return {k: course[k] for k in keys}

    @staticmethod
    def _process_section(section: Dict, units_dict: Dict) -> Dict:
        return {
            'id': int(section['id']),
            'title': section['title'],
            'position': section['position'],
            'course_id': section['course'],
            'lessons': [units_dict[unit] for unit in section['units']]
        }

    @staticmethod
    def _process_unit(unit: Dict) -> Dict:
        return {
            'id': int(unit['id']),
            'position': unit['position'],
            'section_id': unit['section'],
            'lesson_id': unit['lesson']
        }

    @staticmethod
    def _process_lesson(lesson: Dict) -> Dict:
        return {
            'id': int(lesson['id']),
            'title': lesson['title'],
            'steps': lesson['steps']
        }

    @staticmethod
    def _process_step(step: Dict) -> Dict:
        return {
            'id': int(step['id']),
            'lesson_id': step['lesson'],
            'position': step['position'],
            'block_type': step['block']['name'],
            'worth': step['worth']
        }

    # def export_to_csv(self, filename: str = None) -> None:
    #     if not filename:
    #         filename = f'course_{self.course_id}_dump.csv'

    #     with open(filename, 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['Type', 'ID', 'Data'])

    #         for obj_type in ['course', 'sections', 'units', 'lessons', 'steps']:
    #             for item in self._data[obj_type]:
    #                 writer.writerow([obj_type[:-1] if obj_type.endswith('s') else obj_type,
    #                                 item['id'], str(item)])


class Students(StepikAPIClient):
    def __init__(self, token: str, class_id: int):
        super().__init__(token)
        self.class_id = class_id

    def get_students(self) -> List[int]:
        """Получаем список id всех студентов класса"""
        url = f"{self.API_HOST}/api/students"
        params = {'klass': self.class_id, 'page': 1}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return [s['user'] for s in response.json()['students']]
        except (RequestException, JSONDecodeError, KeyError) as e:
            print(f"Error fetching students: {e}")
            return []


class User(StepikAPIClient):
    def get_users_info(self, user_ids: List[int]) -> Dict[int, str]:
        """Получаем пары {id: full_name}"""
        if not user_ids:
            return {}

        users = self._fetch_objects('user', user_ids)
        return {u['id']: u['full_name'] for u in users}


class GradeBook(StepikAPIClient):
    def __init__(self, token: str, course_id: int, class_id: int):
        super().__init__(token)
        self.course_id = course_id
        self.class_id = class_id

    def get_grades(self) -> List[Dict]:
        """Получаем все оценки по классу"""
        url = f"{self.API_HOST}/api/course-grades"
        params = {
            'course': self.course_id,
            'klass': self.class_id,
            'order': '-score,-id',
            'page': 1
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()['course-grades']
        except (RequestException, JSONDecodeError) as e:
            print(f"Error fetching grades: {e}")
            return []
        
    def get_grades_pair(self) -> List[Dict]:
        """Получаем все оценки по классу в виде {stedent_id: [{"score": ..., "step": ...}]}
            None - нет посылок; 0 - посылки были, но верные; все остальное - оценка
        """
        grades = self.get_grades()
        d = dict()
        pr = Parcels(self.token, class_id=self.class_id)
        # Если нет посылок, то ставим None
        for student_grade in grades:
            d[student_grade['user']] = {
                    int(grade['step_id']): (
                        0 if not grade['is_passed'] and grade['total_submissions'] != 0
                        else None if grade['total_submissions'] == 0
                        else int(grade['score'])
                    )
                    for _, grade in student_grade['results'].items()
                }
        return d


    def get_student_grades(self, student_id: int) -> Dict[int, float]:
        """Получаем оценки студента по id"""
        grades = self.get_grades()
        for student_grade in grades:
            if student_grade['user'] == student_id:
                return {
                    int(grade['step_id']): grade['score']
                    for _, grade in student_grade['results'].items()
                }
        return {}


class Parcels(StepikAPIClient):
    """Класс для работы с посылками"""
    def __init__(self, token: str, class_id: int):
        super().__init__(token)
        self.class_id = class_id

    def get_parcels(self, step_id: int, student_id: int):
        """Получаем все посылки по шагу и студенту"""
        url = f"{self.API_HOST}/api/submissions"
        params = {
            'klass': self.class_id,
            'step': step_id,
            'order': 'desc',
            'page': 1
        }
        params = {
            'klass': self.class_id,
            'step': step_id,
            'page': 1,
            'order': 'desc',
            'search': f'id:{student_id}'
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()['submissions']
        except (RequestException, JSONDecodeError) as e:
            print(f"Error fetching parcels: {e}")
            return []
