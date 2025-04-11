import pyparsing as pp
from step_classes import Step


class StepSpace(Step):
    @staticmethod
    def parse(text):
        question = ""
        txt_space = ""
        space_number = 0
        answer = []

        lines = [line for line in text.splitlines()]
        parse_answer = pp.Suppress('ANSWER:') + pp.delimitedList(pp.Word(pp.alphas))

        flag = ''

        for line in lines:
            if parse_answer.matches(line):
                parse_tmp = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())
                line = "ANSWER: " + parse_tmp.parseString(line)[0].replace(' ', '')
                answer_result = parse_answer.parseString(line)

                if len(answer_result.asList()) != space_number:
                    raise ValueError("Incorrect answer")

                ans = {}

                for i in range(len(answer_result.asList())):
                    ans[i + 1] = answer_result[i]

                answer.append(ans)
                continue

            if flag == 'TEXTBEGIN':
                if line.strip() == 'TEXTEND':
                    flag = 'TEXTEND'
                    question += '\n'
                    continue

                if txt_space or line:
                    if txt_space:
                        txt_space += '\n'
                    txt_space += line
                    space_number += len([st for st in line.split() if st in '_' * 100])
                continue

            if line.strip() == 'TEXTBEGIN':
                flag = 'TEXTBEGIN'
                continue

            if flag != 'TEXTEND':
                if question:
                    question += '\n'
                question += line

        return question, txt_space, space_number, answer

    def __init__(self, step_id, title, question, txt_space, space_number, answer):
        super().__init__(step_id, title)
        self.question = question
        self.txt_space = txt_space
        self.space_number = space_number
        self.answer = answer

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "text with space": self.txt_space,
            "space number": self.space_number,
            "answer": self.answer
        }

        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.txt_space:
            raise ValueError("Text with space must not be empty.")
        if self.space_number <= 0:
            raise ValueError("Space number must be more than zero")
        if not self.answer:
            raise ValueError("Answer must not be empty.")
