import pyparsing as pp
from step_classes import Step


class StepString(Step):
    """
    Класс для строковых задач, требующих текстовых ответов.
    """
    def __init__(self, step_id, title, text, regexp=None):
        super().__init__(step_id, title)
        self.text = text
        self.question = ""   # Вопрос для задачи
        self.answer = []      # Правильный ответ
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

    def parse_step(self):
        lines = [line for line in self.text.splitlines()]
        parse_answer = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())

        for line in lines:
            line = line.strip()

            if not self.answer:
                if not parse_answer.matches(line):
                    if self.question:
                        self.question += '\n'
                    self.question += line

            if parse_answer.matches(line):
                answer_result = parse_answer.parseString(line)
                self.answer.append(" ".join(answer_result).strip().lower())
