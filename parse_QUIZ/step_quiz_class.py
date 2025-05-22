from step_classes import Step
import pyparsing as pp


class StepQuiz(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type='QUIZ'):
        question = ""
        possible_answers_tmp = {}
        possible_answers = {}
        shuffle: bool = True
        answer: list = []
        is_mlt = False

        lines = [line for line in text.splitlines()]

        parse_poss_ans = pp.Word(pp.alphas, exact=1) + pp.Suppress(pp.Word(').', exact=1)) + pp.SkipTo(pp.LineEnd())
        parse_shuffle = pp.Suppress('SHUFFLE:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_answer = pp.Suppress('ANSWER:') + pp.delimitedList(pp.Word(pp.alphas, exact=1))

        flag = ''
        tmp = ''

        for line in lines:
            if not answer and not possible_answers_tmp and flag != 'TEXTEND':
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
                        poss_ans = parse_poss_ans.parseString(line.lstrip()).asList()
                        tmp = poss_ans[0]
                        possible_answers_tmp[poss_ans[0]] = poss_ans[1]
                        continue

            if parse_shuffle.matches(line):
                shuffle = (True if parse_shuffle.parseString(line)[0] == 'True' else False)
                continue

            if parse_answer.matches(line):
                parse_tmp = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())
                line = "ANSWER: " + parse_tmp.parseString(line)[0].replace(' ', '')
                answer = parse_answer.parseString(line).asList()

                is_mlt = (len(answer) > 1)

                for key in possible_answers_tmp.keys():
                    possible_answers[possible_answers_tmp[key]] = (key in answer)
                continue

            if tmp:
                if '\n' in possible_answers_tmp[tmp] or line.strip():
                    possible_answers_tmp[tmp] += '\n' + line

        return StepQuiz(step_id, title, question, possible_answers, is_mlt, shuffle)

    def __init__(self, step_id, title, text, possible_answers, is_mlt, shuffle=True):
        super().__init__(step_id, title, text)
        self.possible_answers = possible_answers
        self.shuffle = shuffle
        self.is_mlt = is_mlt

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "name": "quiz",
            "text": self.text,
            "possible answers": self.possible_answers,
            "shuffle": self.shuffle
        }

        return result

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.text:
            raise ValueError("Question must not be empty.")
        if not self.possible_answers:
            raise ValueError("Possible answers must not be empty")
