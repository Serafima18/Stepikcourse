#!/usr/bin/env python3
"""
Главный файл для работы с инструментами создания курсов на Stepik
"""

import requests
import yaml
import json
from pathlib import Path
from typing import Optional, Dict
from lesson_classes import Lesson
from step_classes import Step, StepText, StepNumber, StepikAPI
from h1_h2_steps.h1_h2_steps import parse_text

class StepikCourseTools:
    def __init__(self):
        self.api = StepikAPI()
        self.token = None
        self.course_id = None
        self.lessons = []
        self.current_lesson = None

    def load_credentials(self):
        try:
            with open("creds.yaml", 'r') as f:
                creds = yaml.safe_load(f)
                return creds['client_id'], creds['client_secret']
        except Exception as e:
            print(f"Ошибка загрузки creds.yaml: {e}")
            return None, None

    def authenticate(self):
        client_id, client_secret = self.load_credentials()
        if not client_id or not client_secret:
            print("Не удалось загрузить учетные данные")
            return False
        
        try:
            self.token = self.api.get_token(client_id, client_secret)
            print("Аутентификация прошла успешно")
            return True
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return False

    def parse_step_from_markdown(self, id: int, step_data: Dict) -> Step:
        step_type = step_data['type']
        step_id = id
        title = step_data['header']
        text = step_data['text']
        
        # Вызов строго через Step.parse (он не должен быть переопределён в наследниках)
        return Step.parse(step_id, title, text, step_type.upper())


    def save_lesson_to_markdown(self, lesson: Lesson, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# lesson_id: {lesson.lesson_id}\n\n")
                for step in lesson.steps:
                    f.write(f"## {type(step).__name__.upper()} {step.title}\n")
                    f.write(json.dumps(step.to_json(), ensure_ascii=False, indent=2))
                    f.write("\n\n")
            return True
        except Exception as e:
            print(f"Ошибка сохранения урока: {e}")
            return False

    def save_lessons_to_file(self):
        for lesson in self.lessons:
            filename = f"lesson_{lesson.lesson_id}.md"
            success = self.save_lesson_to_markdown(lesson, filename)
            if success:
                print(f"Урок {lesson.lesson_id} сохранён в {filename}")
            else:
                print(f"Не удалось сохранить урок {lesson.lesson_id}")

    def upload_lesson_from_markdown(self, file_path: str):
        if not self.course_id:
            print("Сначала укажите ID курса")
            return
        try:
            import requests
            from step_classes import StepText
            from step_classes import StepikAPI
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            lesson_data = parse_text(text)

            lesson_id = lesson_data.get("lesson_id")
            steps_raw = lesson_data.get("steps", [])
            if not lesson_id:
                raise ValueError("В Markdown-файле должен быть указан существующий lesson_id для обновления урока.")
            lesson = Lesson(lesson_id=int(lesson_id))

            for idx, step_data in enumerate(steps_raw, start=1):
                step = Step.parse(idx, step_data['header'], step_data['text'], step_data['type'])
                lesson.steps.append(step)

            # Удалено создание нового урока — только обновление существующего
            else:
                lesson.update(self.token)
                print(f"Урок с ID {lesson.lesson_id} обновлён")

            lesson.add_to_course(self.course_id, self.token)
            print(f"Урок добавлен в курс {self.course_id}")

            for idx, step in enumerate(lesson.steps, start=1):
                try:
                    step_url = f"https://stepik.org/lesson/{lesson.lesson_id}/step/{idx}"
                    step.update(step_url, self.token)
                    print(f"✅ Шаг {idx} успешно обновлён: {step_url}")
                except Exception as step_err:
                    print(f"❌ Ошибка при обновлении шага {idx}: {step_err}")

        except Exception as e:
            print(f"Ошибка при загрузке и публикации урока: {e}")

    def interactive_dialog(self):
        print("=== Stepik Tools ===")
        if not Path("creds.yaml").exists():
            print("Файл creds.yaml не найден")
            return
        if not self.authenticate():
            return
        while True:
            print("\nГлавное меню:")
            print("1. Изменить курс")
            print("2. Загрузить курс и показать шаги")
            print("3. Сохранить все уроки в Markdown")
            print("4. Загрузить и опубликовать lesson.md")
            print("5. Выход")
            choice = input("Выберите действие (1-5): ")
            if choice == '1':
                try:
                    self.course_id = int(input("Введите ID курса: "))
                except ValueError:
                    print("Некорректный ID курса")
            elif choice == '2':
                print("Пункт временно отключен")
            elif choice == '3':
                self.save_lessons_to_file()
            elif choice == '4':
                folder = Path("example")
                md_files = list(folder.glob("*.md"))
                if not md_files:
                    print("В папке example нет .md файлов")
                else:
                    print("Доступные .md файлы:")
                    for idx, f in enumerate(md_files, 1):
                        print(f"{idx}. {f.name}")
                    try:
                        file_name = input("Введите имя файла (например, first_lesson.md): ")
                        selected_path = folder / file_name
                        if selected_path.exists():
                            self.upload_lesson_from_markdown(selected_path)
                        else:
                            print("Файл не найден")
                    except ValueError:
                        print("Ошибка: введите число")
            elif choice == '5':
                print("Завершение работы")
                break
            else:
                print("Некорректный выбор")

if __name__ == '__main__':
    tools = StepikCourseTools()
    tools.interactive_dialog()