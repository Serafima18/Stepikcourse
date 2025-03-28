import requests

'''
Иерархия в степике:
    Classe -> Course -> Section -> Unit -> Steps
'''


#  Работа на уровне класса
class Class:
    def __init__(self, url, token) -> None:
        self.url = url
        self.token = token
        self.response = None

    #  Послать запрос на информацию о классе
    def __fetch(self) -> None:
        if (self.response is not None):
            return

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        self.response = requests.get(self.url, headers=headers)

    #  Получить id класса
    def get_class_id(self) -> int | None:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            return int(answer['classes'][0]['id'])
        else:
            return None

    #  Получить id владельца класса
    def get_owner(self) -> int | None:
        self.__fetch()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['owner']
        else:
            return None

    #  Получить название класса
    def get_title(self) -> str | None:
        self.__fetch()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['title']
        else:
            return None

    #  Получить id класса. Номер курса != id курса
    def get_id_course(self) -> int | None:
        self.__fetch()

        answer = self.response.json()
        if self.response.ok:
            return answer['classes'][0]['course']
        else:
            return None

    #  Получить кол-во учащихся
    def get_students_count(self) -> int | None:
        self.__fetch()

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
    def __fetch(self) -> None:
        if (self.response is not None):
            return

        url = "https://stepik.org/api/courses/" + str(self.course)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(url, headers=headers)

    def get_sections(self) -> list[int] | None:
        '''
        Получить секции(модули) курса
        '''
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['sections']
        else:
            return None

    #  Получить название курса
    def get_title(self) -> str | None:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['title']
        else:
            return None

    #  Получить суммарное кол-во уроков
    def total_units(self) -> int | None:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            return answer['courses'][0]['total_units']
        else:
            return None


#  Работа на уровне модуля
#  Модуль и секция в степике одно и тоже
class Module:
    def __init__(self, token: str, module: str) -> None:
        self.module = module
        self.token = token
        self.units_response = None
        self.lessons_response = None

    def __fetch(self) -> None:
        if (self.units_response is None):
            url = "https://stepik.org/api/sections?ids%5B%5D=" + self.module
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            self.units_response = requests.get(url, headers=headers)
        if (self.lessons_response is None):
            units = self.units_response.json()['sections'][0]['units']
            url = "https://stepik.org/api/units?ids%5B%5D=" + str(units.pop(0))
            url += ''.join(["&ids%5B%5D=" + str(unit) for unit in units])
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            self.lessons_response = requests.get(url, headers=headers)

    #  Получить юниты из секции(модуля)
    def get_units_from_section(self) -> list | None:
        self.__fetch()
        answer = self.units_response.json()
        if self.units_response.ok:
            mod = answer['sections'][0]['units']
            return mod
        else:
            return None

    #  Получить уроки из секции(модуля)
    def get_lessons_from_section(self) -> dict | None:
        self.__fetch()
        '''
        Теперь нужно сопоставить юниту урок
        (не понятно, зачем так сделано, возможно,
        что б можно копировать уроки в другие курсы)
        '''
        answer = self.lessons_response.json()
        if self.lessons_response.ok:
            lessons = dict()
            #  Сопоставление
            for unit in answer["units"]:
                lessons[unit['id']] = unit['lesson']
            return lessons
        else:
            return None

    #  Получить название секции(модуля)
    def get_module_title(self) -> str:
        self.__fetch()

        answer = self.units_response.json()
        if self.units_response.ok:
            mod = answer['sections'][0]['title']
            return mod
        else:
            return None


#  Работа на уровне урока
class Lesson:
    def __init__(self, token: str, lesson: str) -> None:
        self.token = token
        self.lesson = lesson
        self.response = None

    #  Запрос на данные
    def __fetch(self) -> None:
        if (self.response is not None):
            return
        url = "https://stepik.org/api/lessons?ids%5B%5D=" + self.lesson
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(url, headers=headers)

    #  Получить шаги в уроке
    def get_steps_in_lesson(self) -> list | None:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            mod = answer['lessons'][0]['steps']
            return mod
        else:
            return None


#  Работа на уровне шага
class Step:
    def __init__(self, token: str, step: str) -> None:
        self.token = token
        self.step = step
        self.response = None

    def __fetch(self) -> None:
        if (self.response is not None):
            return
        url = "https://stepik.org/api/steps?ids%5B%5D=" + self.step
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        self.response = requests.get(url, headers=headers)

    #  Получить имя в шаге. Через имя можно узнать о типе урока
    def get_name_in_step(self) -> str | None:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            mod = answer['steps'][0]['block']['name']
            return mod
        else:
            return None


#  Работа с табелем успеваемости
class GradeBook:
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

    #  Получить все оценки всех студентов
    def get_all_grades(self) -> list[dict]:
        self.__fetch()
        answer = self.response.json()
        if self.response.ok:
            mod = answer['course-grades']
            return mod
        else:
            return None

    #  Получить все оценки для студента
    def get_student_grades(self, student_id: str) -> dict | None:
        all_grades = self.get_all_grades()
        if (all_grades is None):
            return None
        for i in all_grades:
            if (i['user'] == int(student_id)):
                return i['results']
        return dict()

    #  Получить пары: step_id - score, для студента
    def get_student_score(self, student_id: int) -> list[list] | None:
        grades = self.get_student_grades(student_id)
        if (grades is None):
            return None
        score = []
        for results_id, results in grades.items():
            score.append([results["step_id"], results["score"]])
        return score


#  Класс для работы с пользователями
class User:
    def __init__(self, token: str, user_id: str) -> None:
        self.token = token
        self.user_id = user_id
        self.response = None

    def __fetch(self) -> None:
        if (self.response is not None):
            return
        url = "https://stepik.org/api/users?ids%5B%5D=" + self.user_id
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
    def get_user_name(self) -> str | None:
        info = self.__fetch()
        if (info is None):
            return None
        return info[0]['full_name']
