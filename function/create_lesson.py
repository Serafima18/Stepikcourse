# create_lesson.py
from classes import StepText, Lesson, StepikAPI
import json
from pathlib import Path

def load_token_from_file(token_file=".token"):
    """Загружает токен из файла"""
    token_path = Path(token_file)
    if token_path.exists():
        with open(token_path, 'r') as f:
            return f.read().strip()
    return None

def create_basic_math_lesson():
    # Получаем токен доступа (3 способа)
    token = None
    
    # Способ 1: Загрузить из файла .token (если использовали get_token.py)
    token = load_token_from_file()
    
    # Способ 2: Получить новый токен через StepikAPI
    if not token:
        try:
            token = StepikAPI.get_token()
        except Exception as e:
            print(f"Ошибка получения токена: {str(e)}")
            return None
    
    # ID вашего курса
    COURSE_ID = 232374

    # Создаем шаги для урока "1+1"
    steps = [
        StepText(
            step_id=1,
            title="Введение в сложение",
            content="<p>Давайте научимся складывать числа. Самый простой пример - это 1+1.</p>"
        ),
        StepText(
            step_id=2,
            title="Что такое сложение?",
            content="<p>Сложение - это математическая операция, которая объединяет два числа в одно.</p>"
                    "<p>Когда мы говорим 1+1, мы берем одну единицу и добавляем к ней еще одну единицу.</p>"
        ),
        StepText(
            step_id=3,
            title="Пример 1+1",
            content="<p>Давайте решим пример 1+1:</p>"
                    "<ul>"
                    "<li>Возьмем один предмет (например, яблоко)</li>"
                    "<li>Добавим еще один такой же предмет</li>"
                    "<li>Сколько предметов у нас теперь?</li>"
                    "</ul>"
        ),
        StepText(
            step_id=4,
            title="Ответ",
            content="<p>Правильный ответ: <strong>2</strong></p>"
                    "<p>1 + 1 = 2</p>"
                    "<p>Теперь вы знаете, как решать простейшие примеры на сложение!</p>"
        )
    ]
    
    # Создаем объект урока
    lesson = Lesson(lesson_id=0, steps=steps)
    
    try:
        # 1. Создаем урок
        result = lesson.create(token)
        print(f"Урок успешно создан! ID урока: {lesson.lesson_id}")
        print(f"Предпросмотр: https://stepik.org/lesson/{lesson.lesson_id}")
        
        # 2. Добавляем урок в курс
        try:
            course_result = lesson.add_to_course(COURSE_ID, token)
            print(f"Урок успешно добавлен в курс!")
            print(f"Ссылка на курс: https://stepik.org/course/{COURSE_ID}/syllabus")
        except Exception as course_error:
            print(f"Урок создан, но не добавлен в курс: {str(course_error)}")
            print(f"Вы можете добавить его вручную через интерфейс Stepik")
        
        return lesson
        
    except Exception as e:
        print(f"Ошибка при создании урока: {str(e)}")
        return None

if __name__ == "__main__":
    created_lesson = create_basic_math_lesson()
    if created_lesson:
        print("Урок успешно создан и добавлен в курс!")
    else:
        print("Не удалось создать урок")