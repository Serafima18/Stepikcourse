from StepicAPI.classesAPI import CourseData, User, GradeBook, Students
import json
from jinja2 import Environment, FileSystemLoader
import argparse

#  Получаем аргументы из командно строки
parser = argparse.ArgumentParser()
parser.add_argument('course_id', type=int, help='Id курса')
parser.add_argument('class_id', type=int, help='Id класса')
parser.add_argument(
    'section_id',
    type=int,
    help='Id модуля(для первой версии таблицы)'
)
parser.add_argument(
    '-tp',
    '--table_path',
    type=str,
    default='./HTML/tables/table.html',
    help='Имя файла, куда сохранить табличку'
)
parser.add_argument(
    '--config',
    type=str,
    default='./StepicAPI/config.json',
    help='Путь до конфигурационного файла'
)


#  Разбираем аргументы из командной строки
args = parser.parse_args()
course_id = args.course_id
class_id = args.class_id
section_id = args.section_id
filename = args.table_path
file_conf = args.config

try:
    #  Считываем токен
    with open(file_conf, 'r') as file:
        data = json.load(file)
    token = data['token']

    #  Получаем дфнные курса
    course_data = CourseData(token, course_id=course_id)

    #  Получаем список студентов
    st = Students(token, class_id=class_id)
    students_id = st.get_students()
    students = students_id

    #  Получаем имена
    students_names = User(token)
    students_dict = students_names.get_users_info(students_id)

    #  Получаем оценки
    grade_book = GradeBook(
                    token,
                    course_id=str(course_id),
                    class_id=str(class_id)
                    )
    grades = grade_book.get_grades_pair()

    #  Загружаем и подставляем шаблон
    environment = Environment(loader=FileSystemLoader("./HTML/templates/"))
    template = environment.get_template("table_template.html")
    content = template.render(
        data=course_data.data,
        section_id=section_id,
        students=students_dict,
        grades=grades,
    )

    #  Записываем html-файл
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... записан {filename}")
except FileNotFoundError:
    print(f"Файл {file_conf} не найден.")
