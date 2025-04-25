from step_classes import Step
import pyparsing as pp


class StepMatch(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type=None):
        question = ""
        ln_left = []
        ln_right = []
        answer = {}

        lines = [line for line in text.splitlines()]
        parse_match = pp.Suppress('MATCH')
        parse_answer = pp.Suppress("ANSWER:") + pp.delimitedList(pp.Word(pp.nums + '-'))

        flag = ''
        flag1: bool = True

        for line in lines:
            if flag == 'MATCH':
                line = line.strip()

                if not line:
                    flag = 'END'
                    continue

                if line.replace('—', '') == '':
                    flag1 = False
                    continue

                if line.replace('=', '') == '':
                    flag1 = True
                    continue

                if flag1:
                    ln_left.append(line)
                else:
                    ln_right.append(line)

                continue

            if parse_match.matches(line):
                flag = 'MATCH'
                continue

            if flag != 'END':
                if question:
                    question += '\n'
                question += line

            if parse_answer.matches(line):
                answer_result = parse_answer.parseString(line)

                for ans in answer_result.asList():
                    i = ans.index('-')
                    answer[int(ans[:i])] = int(ans[i + 1:])

        return StepMatch(step_id, title, question, ln_left, ln_right, answer)

    def __init__(self, step_id, title, question, ln_left, ln_right, answer):
        super().__init__(step_id, title)
        self.question = question
        self.ln_left = ln_left
        self.ln_right = ln_right
        self.answer = answer

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "left lines": self.ln_left,
            "right lines": self.ln_right,
            "answer": self.answer
        }

        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.ln_left:
            raise ValueError("Left lines must not be empty")
        if not self.ln_right:
            raise ValueError("Right lines must not be empty")
        if not self.answer:
            raise ValueError("Answer must not be empty.")
