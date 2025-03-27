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