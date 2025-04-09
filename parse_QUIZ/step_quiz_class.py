from step_classes import Step
import pyparsing as pp


class StepQuiz(Step):
    @staticmethod
    def parse(text):
        question = ""
        possible_answers = {}
        shuffle = True
        answer = []

        lines = [line for line in text.splitlines()]

        parse_poss_ans = pp.Word(pp.alphas, exact=1) + pp.Word(').', exact=1) + pp.SkipTo(pp.LineEnd())
        parse_shuffle = pp.Suppress('SHUFFLE:') + pp.SkipTo(pp.LineEnd())
        parse_answer = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())

        flag = ''

        for line in lines:
            line = line.strip()

            if not answer and not possible_answers and flag != 'TEXTEND':
                if line.strip() == 'TEXTBEGIN':
                    flag = 'TEXTBEGIN'
                    continue

                if line.strip() == 'TEXTEND':
                    flag = 'TEXTEND'
                    continue

                if not parse_poss_ans.matches(line.lstrip()) or flag == 'TEXTBEGIN':
                    if question:
                        question += '\n'
                    question += line
                    continue

            if not answer:
                if not parse_answer.matches(line):
                    if parse_poss_ans.matches(line.lstrip()):
                        n = line[0]
                        possible_answers[n] = line[2:].strip()
                        continue

            if parse_shuffle.matches(line):
                if line[8:].strip().lower() == 'false':
                    shuffle = False
                elif line[8:].strip().lower() == 'true':
                    shuffle = True

            if parse_answer.matches(line):
                answer_res = parse_answer.parseString(line)
                answer.append(answer_res[0].strip().split(', '))

        return question, possible_answers, shuffle, answer

    def __init__(self, step_id, title):
        super().__init__(step_id, title)
        self.question = ''
        self.possible_answers = {}
        self.answer = []

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "possible answers": self.possible_answers,
            "answer": self.answer
        }

        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.question:
            raise ValueError("Question must not be empty.")
        if not self.possible_answers:
            raise ValueError("Possible answers must not be empty")
        if not self.answer:
            raise ValueError("Answer must not be empty.")
