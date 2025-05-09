import pyparsing as pp
import re
from step_classes import Step


class StepSpace(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type='SPACE'):
        rus_alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        question = ""
        txt_space = ""
        space_number = 0
        answer = {
            'space with choice': {},
            'space without': {}
        }

        caseless = True
        show_correct = True
        score_formula = True
        score = 0

        lines = [line for line in text.splitlines()]
        parse_spacetext = pp.Suppress('SPACETEXT')
        parse_config = pp.Suppress('CONFIG')
        parse_caseless = pp.Suppress('CASELESS:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_show_correct = pp.Suppress('SHOW_CORRECT:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_score_form = pp.Suppress('SCORE_FORMULA:') + (pp.CaselessLiteral('True') | pp.CaselessLiteral('False'))
        parse_score = pp.Suppress('SCORE:') + pp.Word(pp.nums)
        parse_answer = pp.delimitedList(pp.Word(pp.alphanums + rus_alp + '@'), delim=';')

        flag = ''

        for line in lines:
            if flag == 'SPACETEXT':
                if parse_config.matches(line):
                    flag = 'CONFIG'
                    continue

                if txt_space:
                    txt_space += '\n'

                if '___' in line:
                    inner_content = pp.CharsNotIn("[]")
                    enclosed = pp.Suppress("___[") + inner_content + pp.Suppress("]")

                    extracted_list = enclosed.searchString(line)

                    ln = [item[0] for item in extracted_list]
                    num = len(ln)

                    line = re.sub(r"___\[[^\]]+\]", "___", line)

                    for i in range(num):
                        n = space_number + i + 1
                        tmp = (parse_answer.parseString(ln[i])).asList()

                        if ';@' in ln[i]:
                            answer['space with choice'][n] = {'right ans': [], 'all ans': []}

                            for one_ans in tmp:
                                if not one_ans:
                                    continue

                                if one_ans[0] == '@':
                                    one_ans = one_ans[1:]
                                    answer['space with choice'][n]['right ans'].append(one_ans)

                                answer['space with choice'][n]['all ans'].append(one_ans)
                        else:
                            answer['space without'][n] = tmp

                    txt_space += line
                    space_number += num
                continue

            if parse_spacetext.matches(line):
                flag = 'SPACETEXT'
                continue

            if flag != 'CONFIG':
                if question:
                    question += '\n'
                question += line
                continue

            if parse_caseless.matches(line):
                caseless = parse_caseless.parseString(line)[0]
                continue

            if parse_show_correct.matches(line):
                show_correct = parse_show_correct.parseString(line)[0]
                continue

            if parse_score_form.matches(line):
                score_formula = parse_score_form.parseString(line)[0]
                continue

            if parse_score.matches(line):
                score = int(parse_score.parseString(line)[0])
                continue

        return StepSpace(step_id, title, question, txt_space, space_number,
                         answer, caseless, show_correct, score_formula, score)

    def __init__(self, step_id, title, question, txt_space, space_number,
                 answer, caseless, show_correct, score_formula, score):
        super().__init__(step_id, title)
        self.question = question
        self.txt_space = txt_space
        self.space_number = space_number
        self.answer = answer
        self.caseless = caseless
        self.show_correct = show_correct
        self.score_formula = score_formula
        self.score = score

    def to_json(self):
        result = {
            "id": self.step_id,
            "title": self.title,
            "type": "space",
            "question": self.question,
            "text with space": self.txt_space,
            "space number": self.space_number,
            "answer": self.answer,
            "caseless": self.caseless,
            "show correct": self.show_correct,
            "score formula": self.score_formula,
            "score": self.score
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
