from step_classes import Step
import pyparsing as pp


class StepMatching(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type='MATCHING'):
        question = ''
        pairs = []
        empty_pair = {'first': '', 'second': ''}
        pair = empty_pair.copy()

        lines = [line for line in text.splitlines()]
        parse_match = pp.Suppress('MATCH')
        parse_first_end = pp.Word('-', min=4)
        parse_second_end = pp.Word('=', min=4)

        state = 'BEGIN'

        for line in lines:
            match state:
                case 'BEGIN':
                    if parse_match.matches(line):
                        state = 'FIRST'
                        continue

                    if question:
                        question += '\n'

                    question += line
                case 'FIRST':
                    if parse_first_end.matches(line):
                        state = 'SECOND'
                        continue

                    if pair['first']:
                        pair['first'] += '\n'

                    pair['first'] += line
                case 'SECOND':
                    if parse_second_end.matches(line):
                        state = 'FIRST'
                        pairs.append(pair)
                        pair = empty_pair.copy()
                        continue

                    if pair['second']:
                        pair['second'] += '\n'

                    pair['second'] += line

        return StepMatching(step_id, title, question, pairs)

    def __init__(self, step_id, title, text, pairs):
        super().__init__(step_id, title, text)
        self.pairs = pairs

    def to_json(self):
        return {
            "text": self.text,
            "name": "matching",
            "source": {
                "preserve_firsts_order": True,
                "is_html_enabled": True,
                "pairs": self.pairs
            }
        }

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.text:
            raise ValueError("Question must not be empty.")
        if not self.pairs:
            raise ValueError("Pairs must not be empty")
