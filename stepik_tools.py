#!/usr/bin/env python3
"""
Главный файл для работы с инструментами создания курсов на Stepik
"""

import requests
import yaml
import json
import re
from pathlib import Path
from lesson_classes import Lesson
from step_classes import Step, StepikAPI
from h1_h2_steps.h1_h2_steps import parse_text


class StepikCourseTools:
    def __init__(self):
        self.api = StepikAPI()
        self.token = None
        self.course_id = None
        self.lessons = []
        self.current_lesson = None

    @staticmethod
    def open_file():
        file_name = input("Введите путь к файлу (например, example/example.md): ")

        if not Path(file_name).exists():
            print("Файл не найден")
            return None

        if not re.search(r"\.md$", file_name, re.IGNORECASE):
            print("Это не markdown файл")
            return None
        return file_name

    @staticmethod
    def load_credentials():
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

    @staticmethod
    def save_lesson_to_markdown(lesson: Lesson, filename: str) -> bool:
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

    def upload_lesson_from_markdown(self):
        file_path = self.open_file()

        if not file_path:
            return

        try:
            import requests
            from step_classes import StepText, StepikAPI

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            lesson_data = parse_text(text)

            lesson_id = lesson_data.get("lesson_id")
            lesson_id = int(lesson_id)  # Преобразуем строку в число

            steps_raw = lesson_data.get("steps", [])
            if not lesson_id:
                raise ValueError("В Markdown-файле должен быть указан lesson_id для обновления урока.")

            lesson = Lesson(lesson_id=int(lesson_id))

            for idx, step_data in enumerate(steps_raw, start=1):
                step = Step.parse(idx, step_data['header'], step_data['text'], step_data['type'])
                lesson.steps.append(step)

            lesson.add_to_course(self.course_id, self.token)
            print(f"Урок {lesson.lesson_id} добавлен в курс {self.course_id}")

            # Получение существующих шагов
            response = requests.get(
                f'https://stepik.org/api/lessons/{lesson.lesson_id}',
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }
            )
            response.raise_for_status()
            existing_steps_count = len(response.json()['lessons'][0].get('steps', []))

            print(f"Существующих шагов: {existing_steps_count}")

            # Добавляем шаги
            for idx, step in enumerate(lesson.steps, start=1):
                step_url = f"https://stepik.org/lesson/{lesson.lesson_id}/step/{idx}"
                try:
                    # Пробуем обновить
                    step.update(step_url, self.token)
                    print(f"🔁 Шаг {idx} обновлён")
                except Exception as e:
                    print(f"❌ Ошибка при обновлении шага {idx}: {e}")

        except Exception as e:
            print(f"Ошибка при загрузке и публикации урока: {e}")

    def _handle_step_deletion(self):
        try:
            lesson_id = int(input("Введите ID урока, из которого нужно удалить шаг: "))
            step_pos = int(input("Введите номер шага, который нужно удалить: "))
            step_url = f"https://stepik.org/lesson/{lesson_id}/step/{step_pos}"
            confirm = input(f"Удалить шаг {step_pos} из урока {lesson_id}? (y/n): ").lower()
            if confirm == 'y':
                dummy_step = Step(step_id=0, title="", text="")  # просто для вызова метода
                success = dummy_step.remove(step_url, self.token)
                if success:
                    print(f"✅ Шаг {step_pos} успешно удалён из урока {lesson_id}")
                else:
                    print(f"❌ Не удалось удалить шаг")
            else:
                print("Операция отменена")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _handle_step_update(self):
        try:
            lesson_id = int(input("Введите ID урока, где нужно обновить шаг: "))
            step_pos = int(input("Введите номер шага для обновления: "))

            file = self.open_file()

            if not file:
                return

            # Парсим шаги из файла
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
            lesson_data = parse_text(text)
            steps = lesson_data.get("steps", [])

            if step_pos < 1 or step_pos > len(steps):
                print(f"❌ В файле только {len(steps)} шагов. Указанный шаг {step_pos} вне диапазона.")
                return

            step_data = steps[step_pos - 1]
            step = Step.parse(step_pos, step_data['header'], step_data['text'], step_data['type'])
            step_url = f"https://stepik.org/lesson/{lesson_id}/step/{step_pos}"
            step.update(step_url, self.token)
            print(f"✅ Шаг {step_pos} в уроке {lesson_id} обновлён")

        except Exception as e:
            print(f"Ошибка при обновлении шага: {e}")

    def _handle_step_update_from_file_ids(self):
        try:
            file = self.open_file()

            if not file:
                return

            with open(file, 'r', encoding='utf-8') as f:
                raw_text = f.read()

            # Ищем lesson_id и step_id в тексте
            lesson_id_match = re.search(r'lesson_id\s*:\s*(\d+)', raw_text)
            step_id_match = re.search(r'step_id\s*:\s*(\d+)', raw_text)

            if not lesson_id_match or not step_id_match:
                print("❌ В файле должны быть строки 'lesson_id: N' и 'step_id: M'")
                return

            lesson_id = int(lesson_id_match.group(1))
            step_id = int(step_id_match.group(1))

            parsed = parse_text(raw_text)
            steps = parsed.get("steps", [])
            if not steps:
                print("❌ Файл не содержит шагов")
                return

            step_data = steps[0]
            step = Step.parse(
                step_id=step_id,
                title=step_data['header'],
                text=step_data['text'],
                step_type=step_data['type']
            )

            step_url = f"https://stepik.org/lesson/{lesson_id}/step/{step_id}"
            step.update(step_url, self.token)
            print(f"✅ Шаг {step_id} в уроке {lesson_id} обновлён из файла")

        except Exception as e:
            print(f"🚫 Ошибка при обновлении шага: {e}")

    def _handle_add_step_to_lesson(self):
        try:
            file = self.open_file()

            if not file:
                return

            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()

            parsed = parse_text(text)
            lesson_id = parsed.get("lesson_id")
            if not lesson_id:
                print("❌ В файле должен быть указан lesson_id")
                return
            steps = parsed.get("steps", [])
            if not steps:
                print("❌ В файле не найден шаг")
                return

            for step_data in steps:
                # Определяем позицию — добавляем в конец
                headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }
                response = requests.get(
                    f'https://stepik.org/api/lessons/{lesson_id}',
                    headers=headers
                )
                response.raise_for_status()
                position = len(response.json()['lessons'][0].get('steps', [])) + 1

                step = Step.parse(
                    step_id=0,
                    title=step_data['header'],
                    text=step_data['text'],
                    step_type=step_data['type']
                )

                step.create(lesson_id, position, self.token)
                print(f"✅ Шаг типа {step_data['type']} добавлен в урок {lesson_id} в позицию {position}")

        except Exception as e:
            print(f"🚫 Ошибка при создании шага: {e}")

    def interactive_dialog(self):
        print("=== Stepik Tools ===")

        if not Path("creds.yaml").exists():
            print("Файл creds.yaml не найден")
            return
        if not self.authenticate():
            return

        # Запрашиваем course_id один раз при запуске
        while True:
            try:
                self.course_id = int(input("Введите ID курса: "))
                break
            except ValueError:
                print("Некорректный ID курса, попробуйте ещё раз.")

        while True:
            print("\nГлавное меню:")
            print("1. Создать и загрузить новый урок из Markdown")
            print("2. Обновить существующий урок из Markdown")
            print("3. Добавить шаг в существующий урок")
            print("4. Обновить шаг в уроке (из Markdown)")
            print("5. Удалить шаг из урока")
            print("6. Выход")

            choice = input("Выберите действие (1-6): ")

            if choice == '2':
                self.upload_lesson_from_markdown()

            if choice == '1':
                # self.upload_lesson_from_markdown()
                print("Нереализовано")
                continue

            elif choice == '5':
                self._handle_step_deletion()

            elif choice == '4':
                self._handle_step_update_from_file_ids()

            elif choice == '6':
                print("Завершение работы")
                break

            elif choice == '3':
                self._handle_add_step_to_lesson()

            else:
                print("Некорректный выбор")


if __name__ == '__main__':
    tools = StepikCourseTools()
    tools.interactive_dialog()
