import requests
import re
from requests.exceptions import HTTPError
from base64 import b64encode
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import markdown
from bs4 import BeautifulSoup

class Step:
    """
    Базовый класс для всех шагов.
    """
    def __init__(self, step_id: int, title: str):
        self.step_id = step_id  # Идентификатор шага
        self.title = title  # Название или заголовок шага

    def to_json(self) -> dict:
        """
        Преобразует шаг в формат JSON для отправки на платформу.
        """
        raise NotImplementedError("Subclasses should implement this!")

    def __str__(self) -> str:
        """
        Строковое представление шага.
        """
        return f"{self.title} (ID: {self.step_id})"

    def validate(self) -> None:
        """
        Проверяет, что все необходимые атрибуты были заданы.
        """
        raise NotImplementedError("Subclasses should implement this!")

    @staticmethod
    def _get_lesson_and_position(step_url: str) -> tuple:
        """
        Извлекает ID урока и позицию шага из URL.
        """
        match = re.search(r'lesson/(\d+)/step/(\d+)', step_url)
        if not match:
            raise ValueError("Неверный формат URL шага")
        return match.groups()

    @classmethod
    def get_step_source(cls, step_url: str, token: str) -> dict:
        """
        Получает данные шага с сервера Stepik.
        """
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
        """
        Создает новый шаг в указанном уроке.
        """
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

    def update(self, step_url: str, token: str) -> dict:
        """
        Обновляет существующий шаг на платформе.
        """
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
        """
        Удаляет шаг с платформы.
        """
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


class StepText(Step):
    """
    Класс для шагов с текстовым содержимым.
    """
    def __init__(self, step_id: int, title: str, content: str):
        super().__init__(step_id, title)
        self.content = content  # Текстовое содержание шага

    def to_json(self) -> dict:
        return {
            "name": "text",
            "text": self.content,
            "is_html_enabled": True
        }

    def validate(self) -> None:
        if not self.content:
            raise ValueError("Content must not be empty.")


class StepNumber(Step):
    """
    Класс для числовых задач.
    """
    def __init__(self, step_id: int, title: str, question: str, answer: float, tolerance: float = 0):
        super().__init__(step_id, title)
        self.question = question   # Вопрос для задачи
        self.answer = answer       # Правильный ответ
        self.tolerance = tolerance  # Допустимая погрешность

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


class StepString(Step):
    """
    Класс для строковых задач, требующих текстовых ответов.
    """
    def __init__(self, step_id: int, title: str, question: str, answer: str, regexp: str = None):
        super().__init__(step_id, title)
        self.question = question   # Вопрос для задачи
        self.answer = answer       # Правильный ответ
        self.regexp = regexp       # Регулярное выражение для проверки ответа

    def to_json(self) -> dict:
        result = {
            "name": "string",
            "text": self.question,
            "answer": self.answer,
            "is_html_enabled": True
        }
        if self.regexp:
            result["regexp"] = self.regexp
        return result

    def validate(self) -> None:
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.answer:
            raise ValueError("Answer must not be empty.")
        if self.regexp and not isinstance(self.regexp, str):
            raise ValueError("Regexp must be a string if provided.")


@dataclass
class Lesson:
    """
    Класс для работы с уроками на Stepik.
    """
    lesson_id: int
    steps: List[Step] = field(default_factory=list)

    @classmethod
    def parse(cls, markdown_filename: str) -> 'Lesson':
        """
        Разбирает маркдаун файл и возвращает объект Lesson.
        """
        with open(markdown_filename, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Пример парсинга
        
        steps = []
        for i, heading in enumerate(soup.find_all(['h1', 'h2', 'h3'])):
            content = str(heading.find_next('p')) if heading.find_next('p') else ""
            steps.append(StepText(i+1, heading.text, content))
        
        return cls(lesson_id=0, steps=steps)

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
    
    
    def add_to_course(self, course_id: int, token: str) -> dict:
        """
        Добавляет урок в указанный курс
        """
        if not self.lesson_id:
            raise ValueError("Lesson ID is not set. Create lesson first.")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'course': course_id,
            'lesson': self.lesson_id
        }
        
        response = requests.post(
            'https://stepik.org/api/course-lessons',
            json=data,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def add_to_course(self, course_id: int, token: str, section_id: int = None, position: int = 1) -> dict:
        """
        Добавляет урок в указанный курс через API units
        
        Args:
            course_id: ID курса
            token: API токен
            section_id: ID секции курса (опционально)
            position: Позиция в секции (по умолчанию 1)
            
        Returns:
            Ответ API в формате JSON
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


class StepikAPI:
    """
    Класс для работы с API Stepik.
    """
    @staticmethod
    def get_token() -> str:
        """
        Получает access token из creds.yaml.
        """
        creds_path = Path("creds.yaml")
        
        if not creds_path.exists():
            raise FileNotFoundError("Файл creds.yaml не найден")
        
        with open(creds_path, 'r') as f:
            creds = yaml.safe_load(f)
            client_id = creds["client_id"]
            client_secret = creds["client_secret"]
        
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
            raise Exception(f"Ошибка получения токена: {response.text}")
        
class StepikAPI:
    """
    Класс для работы с API Stepik.
    """
    @staticmethod
    def get_token(client_id: str = None, client_secret: str = None) -> str:
        """
        Получает access token из creds.yaml или использует переданные credentials.
        Поддерживает два метода аутентификации: Basic Auth и через заголовок Authorization.
        """
        # Если credentials не переданы, пытаемся загрузить из creds.yaml
        if client_id is None or client_secret is None:
            try:
                creds_path = Path("creds.yaml")
                with open(creds_path, 'r') as f:
                    creds = yaml.safe_load(f)
                    client_id = creds["client_id"]
                    client_secret = creds["client_secret"]
            except Exception as e:
                raise ValueError("Не удалось загрузить credentials. Укажите client_id и client_secret вручную или создайте creds.yaml") from e
        
        # Метод 1: Используем HTTP Basic Auth (как в вашем примере)
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        response = requests.post(
            'https://stepik.org/oauth2/token/',
            data={'grant_type': 'client_credentials'},
            auth=auth
        )
        
        # Метод 2: Альтернативный способ с Base64 в заголовке
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