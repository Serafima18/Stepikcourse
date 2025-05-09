import pyparsing as pp
from step_classes import Step


class StepString(Step):
    """
    Класс для строковых задач, требующих текстовых ответов.
    """

    @classmethod
    def parse(cls, step_id, title, text, step_type='STRING'):
        question = ""
        answer: str = ''
        regexp = None

        lines = [line for line in text.splitlines()]
        parse_answer = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())
        parse_regexp = pp.Suppress("REGEX:") + pp.SkipTo(pp.LineEnd())

        for line in lines:
            if not answer:
                if not parse_answer.matches(line):
                    if question:
                        question += '\n'
                    question += line

            if parse_answer.matches(line):
                answer = parse_answer.parseString(line)[0]

            if parse_regexp.matches(line):
                regexp = parse_regexp.parseString(line)[0]

        return StepString(step_id, title, question, answer, regexp)

    def __init__(self, step_id, title, question, answer, regexp=None):
        super().__init__(step_id, title)
        self.question = question
        self.answer = answer
        self.regexp = regexp

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "answer": self.answer
        }

        if self.regexp:
            result["regexp"] = self.regexp
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
