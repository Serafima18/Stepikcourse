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
        Добавляет урок в указанный курс через API units
        """
        if not self.lesson_id:
            raise ValueError("Lesson ID is not set. Create lesson first.")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Сначала получаем первую секцию курса, если section_id не указан
        if section_id is None:
            sections_response = requests.get(
                f'https://stepik.org/api/sections?course={course_id}',
                headers=headers
            )
            sections_response.raise_for_status()
            sections = sections_response.json().get('sections', [])
            
            if not sections:
                raise ValueError(f"В курсе {course_id} нет секций")
                
            section_id = sections[0]['id']
        
        # Создаем unit (связь между уроком и секцией курса)
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