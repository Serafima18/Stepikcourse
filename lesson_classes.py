import requests
from typing import List
from dataclasses import dataclass, field
from step_classes import Step  # Импортируем базовый класс Step


@dataclass
class Lesson:
    """
    Класс для операций с уроками на Stepik (создание, обновление, удаление)
    """
    lesson_id: int
    steps: List[Step] = field(default_factory=list)

    def create(self, token: str) -> dict:
        """
        Создает новый урок на Stepik.
        """
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'lesson': {
                'title': f'Урок с {len(self.steps)} шагами',
                'steps': [step.to_json() for step in self.steps]
            }
        }

        response = requests.post(
            'https://stepik.org/api/lessons',
            json=data,
            headers=headers
        )
        response.raise_for_status()

        result = response.json()
        self.lesson_id = result['lessons'][0]['id']
        return result

    def update(self, token: str) -> dict:
        """
        Обновляет урок на Stepik.
        """
        if not self.lesson_id:
            raise ValueError("Lesson ID is not set. Create lesson first.")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'lesson': {
                'id': self.lesson_id,
                'title': f'Обновленный урок с {len(self.steps)} шагами',
                'steps': [step.to_json() for step in self.steps]
            }
        }

        response = requests.put(
            f'https://stepik.org/api/lessons/{self.lesson_id}',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def remove(self, token: str) -> bool:
        """
        Удаляет урок с Stepik.
        """
        if not self.lesson_id:
            raise ValueError("Lesson ID is not set.")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.delete(
            f'https://stepik.org/api/lessons/{self.lesson_id}',
            headers=headers
        )
        return response.status_code == 204

    def add_to_course(self, course_id: int, token: str, section_id: int = None, position: int = 1) -> dict:
        """
        Добавляет урок в указанный курс через API units.
        Не создаёт секцию и unit повторно, если урок уже добавлен.
        """
        if not self.lesson_id:
            raise ValueError("Lesson ID is not set. Create lesson first.")

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Проверка: уже добавлен ли урок в курс?
        units_response = requests.get(
            f"https://stepik.org/api/units?lesson={self.lesson_id}",
            headers=headers
        )
        units_response.raise_for_status()
        units = units_response.json().get("units", [])

        for unit in units:
            # Проверяем, связан ли урок с нужным курсом
            section_id_from_unit = unit.get("section")
            if section_id_from_unit:
                section_resp = requests.get(
                    f"https://stepik.org/api/sections/{section_id_from_unit}",
                    headers=headers
                )
                section_resp.raise_for_status()
                section = section_resp.json().get("sections", [])[0]
                if section.get("course") == course_id:
                    print(f"📎 Урок уже добавлен в курс {course_id}, секция ID {section_id_from_unit}")
                    return unit  # уже привязан — ничего не делаем

        # Получаем секцию, если не указана
        if section_id is None:
            sections_response = requests.get(
                'https://stepik.org/api/sections',
                params={'course': course_id, 'page': 1},
                headers=headers
            )
            sections_response.raise_for_status()
            sections = sections_response.json().get('sections', [])

            if not sections:
                print(f"⚠️ В курсе {course_id} нет секций. Создаю секцию 'Автосекция'...")
                section_data = {
                    "section": {
                        "course": course_id,
                        "title": "Автосекция",
                        "position": 1
                    }
                }
                create_section_response = requests.post(
                    'https://stepik.org/api/sections',
                    json=section_data,
                    headers=headers
                )
                create_section_response.raise_for_status()
                section_id = create_section_response.json()["sections"][0]["id"]
                print(f"✅ Секция создана с ID {section_id}")
            else:
                section_id = sections[0]['id']

        # Создаем unit только если его ещё нет
        data = {
            'unit': {
                'section': section_id,
                'lesson': self.lesson_id,
                'position': position
            }
        }

        response = requests.post(
            'https://stepik.org/api/units',
            json=data,
            headers=headers
        )

        if response.status_code != 201:
            raise Exception(f"Ошибка добавления урока в курс: {response.status_code} {response.text}")

        return response.json()