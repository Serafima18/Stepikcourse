from step_classes import Step
import pyparsing as pp


class StepQuiz(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type=None):
        question = ""
        possible_answers = {}
        shuffle = True
        answer = []

        lines = [line for line in text.splitlines()]

        parse_poss_ans = pp.Word(pp.alphas, exact=1) + pp.Suppress(pp.Word(').', exact=1)) + pp.SkipTo(pp.LineEnd())
        parse_shuffle = pp.Suppress('SHUFFLE:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_answer = pp.Suppress('ANSWER:') + pp.delimitedList(pp.Word(pp.alphas, exact=1))

        flag = ''
        tmp = ''

        for line in lines:
            if not answer and not possible_answers and flag != 'TEXTEND':
                if line.strip() == 'TEXTBEGIN':
                    flag = 'TEXTBEGIN'
                    continue

                if line.strip() == 'TEXTEND':
                    flag = 'TEXTEND'
                    question += '\n'
                    continue

                if not parse_poss_ans.matches(line.lstrip()) or flag == 'TEXTBEGIN':
                    if question:
                        question += '\n'
                    question += line
                    continue

            if not answer:
                if not parse_answer.matches(line):
                    if parse_poss_ans.matches(line.lstrip()):
                        poss_ans = parse_poss_ans.parseString(line.lstrip())
                        tmp = poss_ans[0]
                        possible_answers[poss_ans[0]] = poss_ans[1].strip()
                        continue

            if parse_shuffle.matches(line):
                shuffle = parse_shuffle.parseString(line)[0]
                continue

            if parse_answer.matches(line):
                parse_tmp = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())
                line = "ANSWER: " + parse_tmp.parseString(line)[0].replace(' ', '')
                answer_res = parse_answer.parseString(line)
                answer.append(answer_res.asList())
                continue

            if tmp:
                if '\n' in possible_answers[tmp] or line.strip():
                    possible_answers[tmp] += '\n' + line

        return StepQuiz(step_id, title, question, possible_answers, answer, shuffle)

    def __init__(self, step_id, title, question, possible_answers, answer, shuffle=True):
        super().__init__(step_id, title)
        self.question = question
        self.possible_answers = possible_answers
        self.shuffle = shuffle
        self.answer = answer

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "string",
            "question": self.question,
            "possible answers": self.possible_answers,
            "shuffle": self.shuffle,
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
