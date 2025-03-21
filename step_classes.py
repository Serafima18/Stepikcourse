class Step:
    """
    Базовый класс для всех шагов.
    """
    def __init__(self, step_id, title):
        self.step_id = step_id  # Идентификатор шага
        self.title = title  # Название или заголовок шага

    def to_json(self):
        """
        Преобразует шаг в формат JSON для отправки на платформу.
        """
        raise NotImplementedError("Subclasses should implement this!")

    def __str__(self):
        """
        Строковое представление шага.
        """
        return f"{self.title} (ID: {self.step_id})"

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты были заданны.
        """
        raise NotImplementedError("Subclasses should implement this!")


class StepText(Step):
    """
    Класс для шагов с текстовым содержимым.
    """
    def __init__(self, step_id, title, content):
        super().__init__(step_id, title)  # Инициализация базового класса
        self.content = content  # Текстовое содержание шага

    def to_json(self):
        """
        Преобразует шаг с текстом в формат JSON для отправки на платформу.
        """
        return {
            "id": self.step_id,
            "title": self.title,
            "type": "text",  # Указываем, что это текстовый шаг
            "content": self.content
        }

    def validate(self):
        """
        Проверяет, что текстовое содержание задано.
        """
        if not self.content:
            raise ValueError("Content must not be empty.")


class StepNumber(Step):
    """
    Класс для числовых задач.
    """
    def __init__(self, step_id, title, question, answer, tolerance=0):
        super().__init__(step_id, title)
        self.question = question   # Вопрос для задачи
        self.answer = answer       # Правильный ответ
        self.tolerance = tolerance  # Допустимая погрешность

    def to_json(self):
        return {
            "id": self.step_id,
            "title": self.title,
            "type": "number",
            "question": self.question,
            "answer": f"{self.answer} ± {self.tolerance}"
        }

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if self.answer is None:
            raise ValueError("Answer must not be None.")
        if self.tolerance < 0:
            raise ValueError("Tolerance must not be negative.")


class StepString(Step):
    """
    Класс для строковых задач, требующих текстовых ответов.
    """
    def __init__(self, step_id, title, question, answer, regexp=None):
        super().__init__(step_id, title)
        self.question = question   # Вопрос для задачи
        self.answer = answer       # Правильный ответ
        self.regexp = regexp       # Регулярное выражение для проверки ответа

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "answer": self.answer
        }
        if self.regexp:
            result["regexp"] = self.regexp  # Добавляем регулярное выражение, если есть
        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.answer:
            raise ValueError("Answer must not be empty.")
        if self.regexp and not isinstance(self.regexp, str):
            raise ValueError("Regexp must be a string if provided.")
