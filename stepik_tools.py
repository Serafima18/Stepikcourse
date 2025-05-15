#!/usr/bin/env python3
"""
Главный файл для работы с инструментами создания курсов на Stepik
"""

from lesson_classes import Lesson
from step_classes import StepText, StepNumber, StepString, StepikAPI
from typing import List, Dict, Optional
import yaml
from pathlib import Path
import os

class StepikCourseTools:
    """
    Основной класс для работы с инструментами создания курсов
    """
    def __init__(self):
        self.api = StepikAPI()
        self.token = None
        self.current_lesson = None
        self.lessons = []  # Список всех созданных уроков
        self.course_id = None  # ID текущего курса

    def load_credentials(self) -> tuple:
        """Загрузка учетных данных из creds.yaml"""
        try:
            with open("creds.yaml", 'r') as f:
                creds = yaml.safe_load(f)
                return creds['client_id'], creds['client_secret']
        except Exception as e:
            print(f"Ошибка загрузки creds.yaml: {str(e)}")
            return None, None
    
    def authenticate(self) -> bool:
        """Аутентификация на Stepik"""
        client_id, client_secret = self.load_credentials()
        if not client_id or not client_secret:
            print("Не удалось загрузить учетные данные")
            return False
        
        try:
            self.token = self.api.get_token(client_id, client_secret)
            if self.token:
                print("Аутентификация прошла успешно!")
                return True
            else:
                print("Ошибка аутентификации")
                return False
        except Exception as e:
            print(f"Ошибка аутентификации: {str(e)}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """Проверка аутентификации"""
        if not self.token:
            if not self.authenticate():
                print("Необходима аутентификация для выполнения этой операции")
                return False
        return True
    
    def check_credentials_file(self) -> bool:
        """Проверка наличия файла с учетными данными"""
        creds_path = Path("creds.yaml")
        if not creds_path.exists():
            return False
        
        try:
            with open(creds_path, 'r') as f:
                creds = yaml.safe_load(f)
                if not creds or 'client_id' not in creds or 'client_secret' not in creds:
                    return False
            return True
        except Exception:
            return False
    
    def create_credentials_file(self) -> bool:
        """Создание файла с учетными данными"""
        client_id = input("Введите ваш client_id: ")
        client_secret = input("Введите ваш client_secret: ")
        
        try:
            with open("creds.yaml", 'w') as f:
                yaml.dump({
                    'client_id': client_id,
                    'client_secret': client_secret
                }, f)
            return True
        except Exception as e:
            print(f"Ошибка при создании файла: {str(e)}")
            return False
    
    def create_lesson_from_markdown(self, md_file: str) -> Lesson:
        """Создание урока из markdown-файла"""
        return Lesson.parse(md_file)
    
    def create_new_lesson(self) -> Lesson:
        """Создание нового урока"""
        title = input("Введите название урока: ")
        lesson = Lesson(lesson_id=0)
        return lesson
    
    def publish_lesson(self, lesson: Lesson) -> Dict:
        """Публикация урока на Stepik"""
        if not self.token:
            raise ValueError("Необходимо сначала аутентифицироваться")
        return lesson.create(self.token)
    
    def add_step_to_lesson(self, lesson: Lesson):
        """Добавление шага к уроку"""
        print("\nДоступные типы шагов:")
        print("1. Текстовый шаг (text)")
        print("2. Шаг с числовым ответом (number)")
        print("3. Шаг с текстовым ответом (string)")
        
        step_choice = input("Выберите тип шага (1-3): ")
        step_type = {
            '1': 'TEXT',
            '2': 'NUMBER',
            '3': 'STRING'
        }.get(step_choice, 'TEXT')
        
        title = input("Введите заголовок шага: ")
        content = input("Введите содержание шага: ")
        
        if step_type == 'NUMBER':
            try:
                answer = float(input("Введите правильный ответ (число): "))
                tolerance = float(input("Введите допустимую погрешность (по умолчанию 0): ") or "0")
                step = StepNumber(
                    step_id=len(lesson.steps) + 1,
                    title=title,
                    question=content,
                    answer=answer,
                    tolerance=tolerance
                )
            except ValueError:
                print("Ошибка: введите корректное число")
                return
        elif step_type == 'STRING':
            answer = input("Введите правильный ответ (текст): ")
            regexp = input("Введите регулярное выражение для проверки (опционально): ") or None
            step = StepString(
                step_id=len(lesson.steps) + 1,
                title=title,
                question=content,
                answer=answer,
                regexp=regexp
            )
        else:
            step = StepText(
                step_id=len(lesson.steps) + 1,
                title=title,
                content=content
            )
        
        lesson.steps.append(step)
        print(f"\nШаг '{title}' успешно добавлен к уроку!")
    
    def remove_step_from_lesson(self, lesson: Lesson):
        """Удаление шага из урока"""
        if not lesson.steps:
            print("В уроке нет шагов для удаления")
            return
        
        print("\nСписок шагов в уроке:")
        for i, step in enumerate(lesson.steps, 1):
            print(f"{i}. {step.title} ({type(step).__name__})")
        
        try:
            step_num = int(input("Введите номер шага для удаления: ")) - 1
            if 0 <= step_num < len(lesson.steps):
                removed_step = lesson.steps.pop(step_num)
                print(f"Шаг '{removed_step.title}' удален")
            else:
                print("Неверный номер шага")
        except ValueError:
            print("Ошибка: введите число")
    
    def update_step_in_lesson(self, lesson: Lesson):
        """Обновление шага в уроке"""
        if not lesson.steps:
            print("В уроке нет шагов для обновления")
            return
        
        print("\nСписок шагов в уроке:")
        for i, step in enumerate(lesson.steps, 1):
            print(f"{i}. {step.title} ({type(step).__name__})")
        
        try:
            step_num = int(input("Введите номер шага для обновления: ")) - 1
            if 0 <= step_num < len(lesson.steps):
                step = lesson.steps[step_num]
                print(f"\nРедактирование шага: {step.title}")
                
                new_title = input(f"Новый заголовок [{step.title}]: ") or step.title
                if isinstance(step, StepText):
                    new_content = input(f"Новое содержание [{step.content}]: ") or step.content
                    step.title = new_title
                    step.content = new_content
                elif isinstance(step, StepNumber):
                    new_question = input(f"Новый вопрос [{step.question}]: ") or step.question
                    new_answer = input(f"Новый ответ [{step.answer}]: ") or step.answer
                    new_tolerance = input(f"Новая погрешность [{step.tolerance}]: ") or step.tolerance
                    step.title = new_title
                    step.question = new_question
                    step.answer = float(new_answer)
                    step.tolerance = float(new_tolerance)
                elif isinstance(step, StepString):
                    new_question = input(f"Новый вопрос [{step.question}]: ") or step.question
                    new_answer = input(f"Новый ответ [{step.answer}]: ") or step.answer
                    new_regexp = input(f"Новое регулярное выражение [{step.regexp}]: ") or step.regexp
                    step.title = new_title
                    step.question = new_question
                    step.answer = new_answer
                    step.regexp = new_regexp
                
                print("Шаг успешно обновлен!")
            else:
                print("Неверный номер шага")
        except ValueError:
            print("Ошибка: введите число")
    
    def show_lesson_steps(self, lesson: Lesson):
        """Показать шаги урока"""
        if not lesson.steps:
            print("В уроке пока нет шагов")
            return
        
        print(f"\nШаги урока '{lesson.lesson_id}':")
        for i, step in enumerate(lesson.steps, 1):
            print(f"{i}. {step.title} ({type(step).__name__})")
            if isinstance(step, StepText):
                print(f"   Содержание: {step.content[:50]}...")
            elif isinstance(step, (StepNumber, StepString)):
                print(f"   Вопрос: {step.question[:50]}...")
                print(f"   Ответ: {step.answer}")
                if isinstance(step, StepNumber):
                    print(f"   Погрешность: {step.tolerance}")
                elif step.regexp:
                    print(f"   Регулярное выражение: {step.regexp}")
            print()
    
    def load_config(self):
        """Загружает конфигурацию из файла"""
        try:
            if Path("config.yaml").exists():
                with open("config.yaml", 'r') as f:
                    config = yaml.safe_load(f)
                    self.course_id = config.get('course_id')
                    return True
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {str(e)}")
        return False
    
    def save_config(self):
        """Сохраняет конфигурацию в файл"""
        try:
            with open("config.yaml", 'w') as f:
                yaml.dump({
                    'course_id': self.course_id
                }, f)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {str(e)}")
            return False
        
    def interactive_dialog(self):
        """Основной интерактивный диалог"""
        print("\n=== Stepik Course Tools ===")
        
        # Проверяем наличие creds.yaml
        if not Path("creds.yaml").exists():
            print("Файл creds.yaml не найден. Создайте его с вашими учетными данными Stepik API.")
            print("Формат файла:")
            print("client_id: ваш_client_id")
            print("client_secret: ваш_client_secret")
            return
        
        # Загружаем конфигурацию
        self.load_config()
        
        # Запрашиваем ID курса, если он еще не задан
        if not self.course_id:
            print("\nПеред началом работы укажите ID курса, с которым будете работать.")
            print("ID курса можно найти в URL вашего курса на Stepik (число после /course/)")
            print("Например: https://stepik.org/course/12345/ - ID курса 12345")
            self.course_id = input("Введите ID вашего курса на Stepik: ")
            self.save_config()
        
        print(f"\nРаботаем с курсом ID: {self.course_id}")
        print(f"Ссылка на курс: https://stepik.org/course/{self.course_id}\n")

        # Загружаем сохраненные уроки
        self.load_lessons_from_file()

        # Аутентификация
        if not self.authenticate():
            print("Не удалось аутентифицироваться. Проверьте файл creds.yaml")
            return
        
        # Основное меню
        while True:
            print("\nГлавное меню:")
            print(f"Текущий курс: {self.course_id} (https://stepik.org/course/{self.course_id})")
            print("1. Создать новый урок")
            print("2. Редактировать существующий урок")
            print("3. Опубликовать урок")
            print("4. Изменить текущий курс")
            print("5. Выход")
            
            choice = input("Выберите действие (1-5): ")
            
            if choice == '1':
                self.handle_create_lesson()
            elif choice == '2':
                self.handle_edit_lesson()
            elif choice == '3':
                self.handle_publish_lesson()
            elif choice == '4':
                self.show_course_link()
            elif choice == '5':
                # Сохраняем уроки перед выходом
                self.save_lessons_to_file()
                print("Работа завершена.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def change_course(self):
        """Изменяет текущий курс"""
        new_course_id = input("Введите новый ID курса: ")
        if new_course_id:
            self.course_id = new_course_id
            self.save_config()
            print(f"Теперь работаем с курсом ID: {self.course_id}")
            print(f"Ссылка: https://stepik.org/course/{self.course_id}")
            
    def handle_create_lesson(self):
        """Обработка создания урока"""
        lesson_name = input("Введите название урока: ")
        self.current_lesson = Lesson(lesson_id=0)
        self.lessons.append(self.current_lesson)
        print(f"Урок '{lesson_name}' создан!")
        self.save_lessons_to_file()  # Сохраняем изменения
        self.edit_lesson_menu()
    
    def edit_lesson_menu(self):
        """Меню редактирования урока"""
        while True:
            print("\nМеню редактирования урока:")
            print("1. Добавить шаг")
            print("2. Удалить шаг")
            print("3. Обновить шаг")
            print("4. Просмотреть шаги")
            print("5. Вернуться в главное меню")
            
            choice = input("Выберите действие (1-5): ")
            
            if choice == '1':
                self.add_step_to_lesson(self.current_lesson)
            elif choice == '2':
                self.remove_step_from_lesson(self.current_lesson)
            elif choice == '3':
                self.update_step_in_lesson(self.current_lesson)
            elif choice == '4':
                self.show_lesson_steps(self.current_lesson)
            elif choice == '5':
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def handle_edit_lesson(self):
        """Обработка редактирования существующего урока"""
        if not self.lessons:
            print("У вас нет созданных уроков")
            return
        
        print("\nВаши уроки:")
        for i, lesson in enumerate(self.lessons, 1):
            print(f"{i}. Урок ID: {lesson.lesson_id}, шагов: {len(lesson.steps)}")
        
        try:
            lesson_num = int(input("Выберите номер урока для редактирования (0 для отмены): ")) - 1
            if lesson_num == -1:
                return
            if 0 <= lesson_num < len(self.lessons):
                self.current_lesson = self.lessons[lesson_num]
                self.edit_lesson_menu()
            else:
                print("Неверный номер урока")
        except ValueError:
            print("Ошибка: введите число")
    
    def handle_publish_lesson(self):
        """Обработка публикации урока"""
        if not self.current_lesson:
            print("Нет текущего урока для публикации")
            return
        
        if not self.ensure_authenticated():
            return
        
        try:
            result = self.publish_lesson(self.current_lesson)
            print(f"\nУрок успешно опубликован! ID: {self.current_lesson.lesson_id}")
            print(f"Ссылка: https://stepik.org/lesson/{self.current_lesson.lesson_id}")
            self.save_lessons_to_file()  # Сохраняем изменения после публикации
        except Exception as e:
            print(f"Ошибка публикации: {str(e)}")

    # В класс StepikCourseTools добавьте следующие методы:

    def save_lessons_to_file(self, filename="lessons.yaml"):
        """Сохраняет список уроков в YAML файл"""
        try:
            lessons_data = []
            for lesson in self.lessons:
                lesson_data = {
                    'lesson_id': lesson.lesson_id,
                    'steps': []
                }
                for step in lesson.steps:
                    step_data = {
                        'step_id': step.step_id,
                        'title': step.title,
                        'type': type(step).__name__
                    }
                    if isinstance(step, StepText):
                        step_data['content'] = step.content
                    elif isinstance(step, StepNumber):
                        step_data.update({
                            'question': step.question,
                            'answer': step.answer,
                            'tolerance': step.tolerance
                        })
                    elif isinstance(step, StepString):
                        step_data.update({
                            'question': step.question,
                            'answer': step.answer,
                            'regexp': step.regexp
                        })
                    lesson_data['steps'].append(step_data)
                lessons_data.append(lesson_data)
            
            with open(filename, 'w') as f:
                yaml.dump(lessons_data, f)
            return True
        except Exception as e:
            print(f"Ошибка сохранения уроков: {str(e)}")
            return False

    def load_lessons_from_file(self, filename="lessons.yaml"):
        """Загружает список уроков из YAML файла"""
        try:
            if not Path(filename).exists():
                return False
                
            with open(filename, 'r') as f:
                lessons_data = yaml.safe_load(f) or []
            
            self.lessons = []
            for lesson_data in lessons_data:
                lesson = Lesson(lesson_data['lesson_id'])
                for step_data in lesson_data['steps']:
                    step_type = step_data.get('type', 'StepText')
                    if step_type == 'StepText':
                        step = StepText(
                            step_id=step_data['step_id'],
                            title=step_data['title'],
                            content=step_data['content']
                        )
                    elif step_type == 'StepNumber':
                        step = StepNumber(
                            step_id=step_data['step_id'],
                            title=step_data['title'],
                            question=step_data['question'],
                            answer=step_data['answer'],
                            tolerance=step_data['tolerance']
                        )
                    elif step_type == 'StepString':
                        step = StepString(
                            step_id=step_data['step_id'],
                            title=step_data['title'],
                            question=step_data['question'],
                            answer=step_data['answer'],
                            regexp=step_data.get('regexp')
                        )
                    lesson.steps.append(step)
                self.lessons.append(lesson)
            
            if self.lessons:
                self.current_lesson = self.lessons[-1]
            return True
        except Exception as e:
            print(f"Ошибка загрузки уроков: {str(e)}")
            return False
        
    def show_course_link(self):
        """Показывает ссылку на курс на Stepik"""
        if not self.lessons:
            print("У вас пока нет опубликованных уроков.")
            return
        
        print("\nВаши опубликованные уроки на Stepik:")
        for lesson in self.lessons:
            if lesson.lesson_id and lesson.lesson_id != 0:
                print(f"Урок ID {lesson.lesson_id}: https://stepik.org/lesson/{lesson.lesson_id}")
        
        # Если есть текущий курс (можно добавить сохранение course_id в класс)
        course_id = input("\nВведите ID вашего курса на Stepik (если есть): ")
        if course_id:
            print(f"\nСсылка на ваш курс: https://stepik.org/course/{course_id}")
        else:
            print("\nЧтобы просмотреть курс, вам нужно знать его ID. "
                "Он доступен в URL вашего курса на Stepik.")

def main():
    """Точка входа для командной строки"""
    tools = StepikCourseTools()
    tools.interactive_dialog()

if __name__ == '__main__':
    main()