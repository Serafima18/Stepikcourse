from StepicAPI.classesAPI import CourseData, User, GradeBook, Students
from StepicAPI.get_my_token import get_token, InvalidToken
from jinja2 import Environment, FileSystemLoader
from progress.bar import IncrementalBar
import argparse
import json


def get_module_grades(students_dict, data, grades):
    '''Получение сумарных оценок учеников по модулям'''
    module_grades = {}
    for student in students_dict:
        gr_dict = {}
        total_sum = 0
        for section in data['course']['sections']:
            sum_grades = 0
            for lesson in data['sections'][section]['lessons']:
                for step in data["lessons"][lesson]["steps"]:
                    if step in grades[student] and data['steps'][step]['block_type'] != "text":
                        if grades[student][step] is not None:
                            sum_grades += grades[student][step]
            gr_dict[section] = sum_grades
            total_sum += sum_grades
        gr_dict['total_sum'] = total_sum
        module_grades[int(student)] = gr_dict
    return module_grades


TEMPLATES_DIR = "./HTML/templates/"
TABLE_TEMPLATE = "table_template.html"

if __name__ == '__main__':
    #  progress bar
    bar = IncrementalBar('Progress', max=8)

    #  Получаем аргументы из командно строки
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        default='./config.json',
        help='Путь до конфигурационного файла'
    )
    parser.add_argument(
        '-tp',
        '--table_path',
        type=str,
        default='./HTML/tables/table.html',
        help='Имя файла, куда сохранить табличку'
    )

    #  Разбираем аргументы из командной строки
    args = parser.parse_args()
    filename = args.table_path
    file_conf = args.config

    try:
        #  Считываем данные из файла конфигурации
        with open(file_conf, 'r') as file:
            data = json.load(file)
        bar.next()
        course_id = data["course_id"]
        class_id = data["class_id"]
        client_id = data["client_id"]
        client_secret = data["client_secret"]

        #  Получаем токен
        token = get_token(client_id, client_secret)
        bar.next()

        #  Получаем данные курса
        course_data = CourseData(token, course_id=course_id)
        bar.next()

        #  Получаем список студентов
        st = Students(token, class_id=class_id)
        students_id = st.get_students()
        students = students_id
        bar.next()

        #  Получаем имена
        students_names = User(token)
        students_dict = students_names.get_users_info(students_id)
        bar.next()

        #  Получаем оценки
        grade_book = GradeBook(
                        token,
                        course_id=str(course_id),
                        class_id=str(class_id)
                        )
        grades = grade_book.get_grades_pair()
        bar.next()

        #  Загружаем и подставляем шаблон
        environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = environment.get_template(TABLE_TEMPLATE)
        print('OK')
        content = template.render(
            data=course_data.data,
            students=students_dict,
            grades=grades,
            class_id=class_id,
            module_grades=get_module_grades(
                                    students_dict,
                                    course_data.data,
                                    grades)
        )
        bar.next()

        #  Записываем html-файл
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            bar.next()
    except FileNotFoundError:
        print(f"Файл {file_conf} не найден.")
    except KeyError as e:
        print(f'В файле {file_conf} нет элемента с ключом {e}')
    except InvalidToken as e:
        print(e)
    except Exception as e:
        print(f"Ошибка: {str(e)}")
