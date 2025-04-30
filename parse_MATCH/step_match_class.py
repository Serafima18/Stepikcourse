from step_classes import Step
import pyparsing as pp


class StepMatching(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type=None):
        question = ""
        pairs = []

        lines = [line for line in text.splitlines()]
        parse_match = pp.Suppress('MATCH')

        flag = ''
        flag1: bool = True
        tmp_ln: bool = False
        pair = {'first': '', 'second': ''}

        for line in lines:
            if flag == 'MATCH':
                line = line.strip()

                if not line:
                    flag = 'END'
                    continue

                if line.replace('—', '') == '':
                    flag1 = False
                    tmp_ln = False
                    continue

                if line.replace('=', '') == '':
                    pairs.append(pair)
                    pair = {'first': '', 'second': ''}

                    flag1 = True
                    tmp_ln = False
                    continue

                if tmp_ln:
                    if flag1:
                        pair['first'] += '\n' + line
                    else:
                        pair['second'] += '\n' + line

                    continue

                if flag1:
                    pair['first'] += line
                else:
                    pair['second'] += line

                tmp_ln = True
                continue

            if parse_match.matches(line):
                flag = 'MATCH'
                continue

            if flag != 'END':
                if question:
                    question += '\n'
                question += line

        return StepMatching(step_id, title, question, pairs)

    def __init__(self, step_id, title, question, pairs):
        super().__init__(step_id, title)
        self.question = question
        self.pairs = pairs

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "matching",
            "question": self.question,
            "pairs": self.pairs
        }

        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.pairs:
            raise ValueError("Pairs must not be empty")
