from step_classes import Step
import pyparsing as pp
from markdown import markdown


class StepQuiz(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type='QUIZ'):
        question = ""
        possible_answers_tmp = {}
        possible_answers = []
        shuffle: bool = True
        answer: list = []
        is_mlt = False

        lines = [line for line in text.splitlines()]

        parse_poss_ans = pp.Word(pp.alphas, exact=1) + pp.Suppress(pp.Word(').', exact=1)) + pp.SkipTo(pp.StringEnd())
        parse_shuffle = pp.Suppress('SHUFFLE:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_answer = pp.Suppress('ANSWER:') + pp.delimitedList(pp.Word(pp.alphas, exact=1))

        flag = ''
        tmp = ['', False]

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
                        tmp = [poss_ans[1], True]
                        possible_answers_tmp[poss_ans[1]] = poss_ans[0]
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
                    possible_answers.append({"text": markdown(key), "is_correct": False, "feedback": "Wrong"})

                    if possible_answers_tmp[key] in answer:
                        possible_answers[-1]["is_correct"] = True
                        possible_answers[-1]["feedback"] = "Right"
                continue

            if tmp[1]:
                key = tmp[0] + '\n' + line
                possible_answers_tmp[key] = possible_answers_tmp.pop(tmp[0])
                tmp[0] = key

        return StepQuiz(step_id, title, question, possible_answers, is_mlt, shuffle)

    def __init__(self, step_id, title, text, possible_answers, is_mlt, shuffle=True):
        super().__init__(step_id, title, text)
        self.possible_answers = possible_answers
        self.shuffle = shuffle
        self.is_mlt = is_mlt

    def to_json(self):
        block = {
            "name": "choice",
            "text": self.text,
            "source": {
                "options": self.possible_answers,
                "is_multiple_choice": self.is_mlt,
                "is_html_enabled": True,
                "shuffle": self.shuffle,
                "is_always_correct": False,
                "sample_size": len(self.possible_answers),
                "preserve_order": False,
                "is_options_feedback": False
            }
        }

        return block

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.text:
            raise ValueError("Question must not be empty.")
        if not self.possible_answers:
            raise ValueError("Possible answers must not be empty")
