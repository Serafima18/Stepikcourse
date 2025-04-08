from StepicAPI.classesAPI import *
from StepicAPI.config import token
from pprint import pprint

course_data = CourseData(token, course_id=188376)

from jinja2 import Environment, FileSystemLoader

section_id = 371387

st = Students(token, class_id=62475)

students_id = st.get_students()
students = students_id
students_names = User(token)
students_dict = students_names.get_users_info(students_id)

grade_book = GradeBook(token, course_id='188376', class_id='62475')
grades = grade_book.get_grades_pair()

environment = Environment(loader=FileSystemLoader("./HTML/templates/"))
template = environment.get_template("table_template.html")
filename = f"./HTML/tables/table_first.html"
content = template.render(
    data=course_data.data,
    section_id=section_id,
    students=students_dict,
    grades=grades,
)
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    print(f"... wrote {filename}")