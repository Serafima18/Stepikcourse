import requests


#  Работа на уровне класса
class Class:
    #  Послать запрос на информацию о классе
    def __get_request(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        self.response = requests.get(self.url, headers=headers)

    def __init__(self, _url, _token) -> None:
        self.url = _url
        self.token = _token
        self.response = None
        self.struct = None

    #  Получить id класса
    def get_class_id(self):
        self.__get_request()
        answer = self.response.json()
        if self.response.ok:
            return int(answer['classes'][0]['id'])
        else:
            print('error')
            return None

    #  Получить id владельца класса
    def get_owner(self):
        self.__get_request()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['owner']
        else:
            return None

    #  Получить название класса
    def get_title(self):
        self.__get_request()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['title']
        else:
            return None

    #  Получить id класса. Номер курса != id курса
    def get_id_course(self):
        self.__get_request()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['course']
        else:
            return None

    #  Получить кол-во учащихся
    def get_students_count(self):
        self.__get_request()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['students_count']
        else:
            return None


#  Работа на уровне курса
class Course:
    def __init__(self, _course: int, _token: str) -> None:
        self.course = _course
        self.token = _token
        self.response = None

    #  Послать запрос на информацию о курсе
    def __get_struct_request(self):
        url = "https://stepik.org/api/courses/" + str(self.course)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(url, headers=headers)

    #  Получить секции(модули) курса
    def get_sections(self) -> list[int]:
        self.__get_struct_request()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['sections']
        else:
            return None

    #  Получить название курса
    def get_title(self) -> str:
        self.__get_struct_request()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['title']
        else:
            return None

    #  Получить суммарное кол-во уроков
    def total_units(self) -> int:
        self.__get_struct_request()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['total_units']
        else:
            return None


#  Работа на уровне модуля
#  Модуль и секция в степике одно и тоже
class Module:
    def __init__(self, _token: str) -> None:
        self.token = _token
        self.module = None

    #  Получить юниты из секции(модуля)
    def get_units_from_section(self, module: int) -> list:
        url = "https://stepik.org/api/sections?ids%5B%5D=" + str(module)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.module = requests.get(url, headers=headers)
        answer = self.module.json()
        if self.module.ok:
            mod = answer['sections'][0]['units']
            return mod
        else:
            return None

    #  Получить уроки из секции(модуля)
    def get_lessons_from_section(self, module: int) -> list:
        #  Сначала нужно получить юниты из модуля
        units = self.get_units_from_section(str(module))
        units_copy = units.copy()
        '''
        Теперь нужно сопоставить юниту урок
        (не понятно, зачем так сделано, возможно,
        что б можно копировать уроки в другие курсы)
        '''
        url = "https://stepik.org/api/units?ids%5B%5D=" + str(units.pop(0))
        url += ''.join(["&ids%5B%5D=" + str(module) for module in units])
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.modules = requests.get(url, headers=headers)
        answer = self.modules.json()
        if self.modules.ok:
            lessons = []
            #  Сопоставление
            for i in answer["units"]:
                for unit in units_copy:
                    if (i['id'] == unit):
                        lessons.append(i["lesson"])
            return lessons
        else:
            return None

    #  Получить название секции(модуля)
    def get_module_title(self, module: int) -> str:
        url = "https://stepik.org/api/sections?ids%5B%5D=" + str(module)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.modules = requests.get(url, headers=headers)
        answer = self.modules.json()
        if self.modules.ok:
            mod = answer['sections'][0]['title']
            return mod
        else:
            return None


#  Работа на уровне урока
class Lesson:
    def __init__(self, _token: str) -> None:
        self.token = _token

    #  Получить шаги в уроке
    def get_steps_in_lesson(self, lesson: int) -> list:
        url = "https://stepik.org/api/lessons?ids%5B%5D=" + str(lesson)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.steps_in_lesson = requests.get(url, headers=headers)
        answer = self.steps_in_lesson.json()
        if self.steps_in_lesson.ok:
            mod = answer['lessons'][0]['steps']
            return mod
        else:
            return None


#  Работа на уровне шага
class Step:
    def __init__(self, _token: str) -> None:
        self.token = _token

    #  Получить имя в шаге. Через имя можно узнать о типе урока
    def get_name_in_step(self, step: int) -> str:
        url = "https://stepik.org/api/steps?ids%5B%5D=" + str(step)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.name_in_step = requests.get(url, headers=headers)
        answer = self.name_in_step.json()
        if self.name_in_step.ok:
            mod = answer['steps'][0]['block']['name']
            return mod
        else:
            return None

    #  Получить текст из шага
    def get_text_in_step(self, step: int) -> str:
        url = "https://stepik.org/api/steps?ids%5B%5D=" + str(step)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.text_in_step = requests.get(url, headers=headers)
        answer = self.text_in_step.json()
        if self.text_in_step.ok:
            mod = answer['steps'][0]['block']['text']
            return mod
        else:
            return None


#  Работа с табелем успеваемости
class GradeBook:
    def __init__(self, _token: str) -> None:
        self.token = _token

    #  Получить все оценки всех студентов
    def get_all_grades(self, course: int, klass: int) -> list[dict]:
        url = "https://stepik.org/api/course-grades?course=" + str(course) + "&is_teacher=false&klass=" + str(klass) + "&order=-score%2C-id&page=1&search="
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.all_grades = requests.get(url, headers=headers)
        answer = self.all_grades.json()
        if self.all_grades.ok:
            mod = answer['course-grades']
            return mod
        else:
            return None

    #  Получить все оценки для студента
    def get_student_grades(self, course: int, klass: int, student_id: int) -> dict:
        url = "https://stepik.org/api/course-grades?course=" + str(course) + "&is_teacher=false&klass=" + str(klass) + "&order=-score%2C-id&page=1&search="
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.student_grades = requests.get(url, headers=headers)
        answer = self.student_grades.json()
        if self.student_grades.ok:
            grades = answer['course-grades']
            for i in grades:
                if (i['user'] == student_id):
                    return i['results']
            return dict()
        else:
            return None

    #  Получить пары: step_id - score, для студента
    def get_student_score(self, course: int, klass: int, student_id: int) -> list[list]:
        grades = self.get_student_grades(course, klass, student_id)
        if (grades is None):
            return None
        score = []
        for results_id, results in grades.items():
            score.append([results["step_id"], results["score"]])
        return score


#  Класс для работы с пользователями
class User:
    def __init__(self, _token: str) -> None:
        self.token = _token

    def __get_user_info(self, user_id: int) -> list[dict]:
        url = "https://stepik.org/api/users?ids%5B%5D=" + str(user_id)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self._user_info = requests.get(url, headers=headers)
        answer = self._user_info.json()
        if self._user_info.ok:
            return answer['users']
        else:
            return None

    #  Получить имя пользователя
    def get_user_name(self, user_id: int) -> str:
        info = self.__get_user_info(user_id)
        if (info is None):
            return None
        return info[0]['full_name']
