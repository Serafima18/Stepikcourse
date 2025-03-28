# Run with Python 3
# Clone course from one Stepik instance (domain) into another
import csv
import requests
from config import token


class StepikAPI:
    __api_host = 'https://stepik.org'
    
    def __init__(self, token: str, course_id: int) -> None:
        self.token = token
        self.course_id = course_id
        self.data = None

    # 3. Call API (https://stepik.org/api/docs/) using this token.
    def __fetch_object(self, obj_class, obj_id):
        api_url = f'{self.__api_host}/api/{obj_class}s/{obj_id}'
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token})
        if not response.ok:
            raise RuntimeError("__fetch_object") 
        response_json = response.json()
        return response_json[f'{obj_class}s'][0]


    def __fetch_objects(self, obj_class, obj_ids):
        objs = []
        # Fetch objects by 30 items,
        # so we won't bump into HTTP request length limits
        step_size = 30
        for i in range(0, len(obj_ids), step_size):
            obj_ids_slice = obj_ids[i:i + step_size]
            api_url = f'{self.__api_host}/api/{obj_class}s?{'&'.join(f'ids[]={obj_id}'
                                                      for obj_id in obj_ids_slice)}'
            response = requests.get(api_url,
                                    headers={'Authorization': 'Bearer ' + token}
                                    )
            response_json = response.json()
            if not response.ok:
                raise RuntimeError("__fetch_objects")
            objs += response_json[f'{obj_class}s']
        return objs
    
    def __fetch_data(self):
        '''
        Запрос на все данные о курсе
        '''
        course = self.__fetch_object('course', self.course_id)
        sections = self.__fetch_objects('section', course['sections'])
        unit_ids = [unit for section in sections for unit in section['units']]

        units = self.__fetch_objects('unit', unit_ids)
        lessons_ids = [unit['lesson'] for unit in units]

        lessons = self.__fetch_objects('lesson', lessons_ids)
        step_ids = [step for lesson in lessons for step in lesson['steps']]

        steps = self.__fetch_objects('step', step_ids)

        data = []
        idd = course['id']
        course = { key: course[key] for key in ['title', 'summary', 'course_format', 'language', 'requirements', 'workload', 'is_public', 'description', 'certificate', 'target_audience'] }
        row = ['course', idd, course]
        data.append(row)

        for section in sections:
            idd = section['id']
            section = { key: section[key] for key in ['title', 'position', 'course'] }
            row = ['section', idd, section]
            data.append(row)
        for unit in units:
            idd = unit['id']
            unit = { key: unit[key] for key in ['position', 'section', 'lesson'] }
            row = ['unit', idd, unit]
            data.append(row)
        for lesson in lessons:
            idd = lesson['id']
            lesson = { key: lesson[key] for key in ['title', 'is_public', 'language'] }
            row = ['lesson', idd, lesson]
            data.append(row)
        for step in steps:
            idd = step['id']
            step_data = {
            'lesson': step['lesson'],
            'position': step['position'],
            'block_name': step['block']['name']  # Извлекаем только имя из блока
            }
            row = ['step', idd, step_data]
            data.append(row)

        self.data = data
        return data
    
    def get_data(self):
        if self.data is None:
            self.__fetch_data()
        return self.data
    
    def get_sections(self):
        self.get_data()
        sections = [i for i in self.data if i[0] == 'section']
        return sections
    
    def get_lessons(self):
        self.get_data()
        lessons = [i for i in self.data if i[0] == 'lesson']
        return lessons
    
    def get_units(self):
        self.get_data()
        units = [i for i in self.data if i[0] == 'unit']
        return units
    
    def get_steps(self):
        self.get_data()
        steps = [i for i in self.data if i[0] == 'step']
        return steps
    
    def save_to_csv(self):
        # write data to file
        csv_file = open(f'course-{self.course_id}-dump.csv', 'w', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(self.data)
        csv_file.close()

class Students:
    '''
    Класс для работы с учениками класса
    '''
    def __init__(self, token: str, class_id: str) -> None:
        self.token = token
        self.class_id = class_id
        self.__response = None

    def __fetch(self) -> None:
        if (self.__response is not None):
            return
        url = "https://stepik.org/api/students?klass=" + str(self.class_id) + "&page=1"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.__response = requests.get(url, headers=headers)
        if self.__response.ok:
            self.__response = self.__response.json()
        else:
            self.__response = None

    def get_students_id(self) -> str | None:
        '''
        Получить имя пользователя
        '''
        self.__fetch()
        students = self.__response
        if (students is None):
            return None
        id = []
        for i in students['students']:
            id.append(i['user'])
        return id

class User:
    '''
    Класс для работы с пользователями
    '''
    def __init__(self, token: str, user_id: str) -> None:
        self.token = token
        self.user_id = user_id
        self.__response = None

    def __fetch(self) -> None:
        if (self.__response is not None):
            return
        url = "https://stepik.org/api/users?ids%5B%5D=" + self.user_id
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.__response = requests.get(url, headers=headers)
        if self.__response.ok:
            self.__response = self.__response.json()
        else:
            self.__response = None


    def get_user_name(self) -> str | None:
        '''
        Получить имя пользователя
        '''
        self.__fetch()
        user = self.__response
        if (user is None):
            return None
        return user['users'][0]['full_name']

class GradeBook:
    '''
    Работа с табелем успеваемости
    '''
    def __init__(self, token: str, course: str, klass: str) -> None:
        self.token = token
        self.course = course
        self.klass = klass
        self.response = None

    def __fetch(self) -> None:
        if (self.response is not None):
            return
        url = ("https://stepik.org/api/course-grades?course=" + self.course +
               "&is_teacher=false&klass=" + self.klass +
               "&order=-score%2C-id&page=1&search=")
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(url, headers=headers)
        if self.response.ok:
            self.response = self.response.json()
        else:
            self.response = None

    def get_all_grades(self) -> list[dict]:
        '''
        Получить все оценки всех студентов
        '''
        self.__fetch()
        if self.response is None:
            return None
        else:
            return self.response['course-grades']

    def get_student_grades(self, student_id: str) -> dict | None:
        '''
        Получить все оценки для студента
        '''
        all_grades = self.get_all_grades()
        if (all_grades is None):
            return None
        for i in all_grades:
            if (i['user'] == int(student_id)):
                return i['results']
        return dict()

    def get_student_score(self, student_id: int) -> list[list] | None:
        '''
        Получить пары: step_id - score, для студента
        '''
        grades = self.get_student_grades(student_id)
        if (grades is None):
            return None
        score = []
        for results_id, results in grades.items():
            score.append([results["step_id"], results["score"]])
        return score
