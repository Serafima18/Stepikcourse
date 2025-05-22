import requests
import re
from requests.exceptions import HTTPError
from base64 import b64encode
import yaml
from pathlib import Path
from typing import List
from dataclasses import dataclass, field


class Step:
    """
    Базовый класс для всех шагов.
    """
    def __init__(self, step_id: int, title: str, text: str):
        self.step_id = step_id
        self.title = title
        self.text = text

    def to_json(self) -> dict:
        raise NotImplementedError("Subclasses should implement this!")

    def __str__(self) -> str:
        return f"{self.title} (ID: {self.step_id})"

    def validate(self) -> None:
        raise NotImplementedError("Subclasses should implement this!")

    @staticmethod
    def _get_lesson_and_position(step_url: str) -> tuple:
        match = re.search(r'lesson/(\d+)/step/(\d+)', step_url)
        if not match:
            raise ValueError("Неверный формат URL шага")
        return match.groups()

    @classmethod
    def get_step_source(cls, step_url: str, token: str) -> dict:
        lesson_id, step_pos = cls._get_lesson_and_position(step_url)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'https://stepik.org/api/step-sources?lesson={lesson_id}&position={step_pos}',
            headers=headers
        )
        response.raise_for_status()
        step_data = response.json()
        
        if not step_data['step-sources']:
            raise ValueError("Шаг не найден")
            
        return step_data['step-sources'][0]

    def create(self, lesson_id: int, position: int, token: str) -> dict:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'step-source': {
                'block': self.to_json(),
                'lesson': lesson_id,
                'position': position
            }
        }
        
        response = requests.post(
            'https://stepik.org/api/step-sources',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def update_json(self):
        pass

    def update(self, step_url: str, token: str) -> dict:
        self.update_json()
        step_source = self.get_step_source(step_url, token)
        lesson_id, step_pos = self._get_lesson_and_position(step_url)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        update_data = {
            'step-source': {
                'id': step_source['id'],
                'block': self.to_json(),
                'lesson': int(lesson_id),
                'position': int(step_pos)
            }
        }
        
        response = requests.put(
            f'https://stepik.org/api/step-sources/{step_source["id"]}',
            json=update_data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def remove(self, step_url: str, token: str) -> bool:
        step_source = self.get_step_source(step_url, token)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.delete(
            f'https://stepik.org/api/step-sources/{step_source["id"]}',
            headers=headers
        )
        return response.status_code == 204

    @classmethod
    def parse(cls, step_id, title, text, step_type='TEXT'):
        from parse_STRING.step_string_class import StepString
        from parse_QUIZ.step_quiz_class import StepQuiz
        from parse_SPACE.step_space_class import StepSpace
        from parse_MATCH.step_match_class import StepMatching

        if step_type not in ['TEXT', 'STRING', 'NUMBER', 'QUIZ', 'SPACE', 'MATCHING']:
            raise NotImplementedError("Incorrect step type")

        match step_type:
            case 'TEXT':
                return StepText.parse(step_id, title, text)
            case 'STRING':
                return StepString.parse(step_id, title, text)
            case 'NUMBER':
                return StepNumber.parse(step_id, title, text)
            case 'QUIZ':
                return StepQuiz.parse(step_id, title, text)
            case 'SPACE':
                return StepSpace.parse(step_id, title, text)
            case 'MATCHING':
                return StepMatching.parse(step_id, title, text)


class StepText(Step):
    def __init__(self, step_id: int, title: str, text: str):
        super().__init__(step_id, title, text)

    def to_json(self) -> dict:
        return {
            "name": "text",
            "text": self.text,
            "is_html_enabled": True
        }

    def validate(self) -> None:
        if not self.text:
            raise ValueError("Content must not be empty.")


class StepNumber(Step):
    def __init__(self, step_id: int, title: str, question: str, answer: float, tolerance: float = 0):
        super().__init__(step_id, title)
        self.question = question
        self.answer = answer
        self.tolerance = tolerance

    def to_json(self) -> dict:
        return {
            "name": "number",
            "text": self.question,
            "answer": f"{self.answer} ± {self.tolerance}",
            "is_html_enabled": True
        }

    def validate(self) -> None:
        if self.answer is None:
            raise ValueError("Answer must not be None.")
        if self.tolerance < 0:
            raise ValueError("Tolerance must not be negative.")


class StepikAPI:
    @staticmethod
    def get_token(client_id: str = None, client_secret: str = None) -> str:
        if client_id is None or client_secret is None:
            try:
                creds_path = Path("creds.yaml")
                with open(creds_path, 'r') as f:
                    creds = yaml.safe_load(f)
                    client_id = creds["client_id"]
                    client_secret = creds["client_secret"]
            except Exception as e:
                raise ValueError("Не удалось загрузить credentials") from e
        
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        response = requests.post(
            'https://stepik.org/oauth2/token/',
            data={'grant_type': 'client_credentials'},
            auth=auth
        )
        
        if response.status_code != 200:
            auth_str = f"{client_id}:{client_secret}"
            auth_b64 = b64encode(auth_str.encode()).decode()
            
            response = requests.post(
                "https://stepik.org/oauth2/token/",
                headers={
                    "Authorization": f"Basic {auth_b64}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "client_credentials"},
            )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Ошибка получения токена: {response.status_code} {response.text}")