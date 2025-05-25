import pyparsing as pp
from step_classes import Step
from markdown import markdown


class StepSpace(Step):
    @classmethod
    def parse(cls, step_id, title, text, step_type='SPACE'):
        rus_alp = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        question = ""
        txt_space = ""
        components = []
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
                    if txt_space:
                        components.append(
                            {
                                "type": "text",
                                "text": markdown(txt_space).replace("\n", "<br>"),
                                "options": []
                            }
                        )
                    flag = 'CONFIG'
                    continue

                if txt_space:
                    txt_space += '\n'

                if '___' in line:
                    enclosed = pp.Suppress("___[") + pp.CharsNotIn("[]") + pp.Suppress("]")

                    ln = enclosed.searchString(line).asList()

                    for i in range(len(ln)):
                        line_t = list(line)
                        components.append(
                            {
                                "type": "text",
                                "text": markdown(txt_space + line[:line_t.index('_')]).replace("\n", "<br>"),
                                "options": []
                            }
                        )

                        line = line[line_t.index(']') + 1:]
                        txt_space = ""
                        tmp = parse_answer.parseString(ln[i][0]).asList()

                        if ';@' in ln[i][0]:
                            components.append(
                                {
                                    "type": "select",
                                    "options": [],
                                    "text": ""
                                }
                            )

                            for one_ans in tmp:
                                if not one_ans:
                                    continue

                                if one_ans[0] == '@':
                                    components[-1]["options"].append({"text": one_ans[1:], "is_correct": True})
                                else:
                                    components[-1]["options"].append({"text": one_ans, "is_correct": False})
                        else:
                            components.append({
                                "type": "input",
                                "options": [],
                                "text": "",
                            })

                            for one_ans in tmp:
                                components[-1]["options"].append({"text": one_ans, "is_correct": True})
                txt_space = line
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

        return StepSpace(step_id, title, question, components, caseless, show_correct, score_formula, score)

    def __init__(self, step_id, title, text, components, caseless, show_correct, score_formula, score):
        super().__init__(step_id, title, text)
        self.components = components
        self.caseless = caseless
        self.show_correct = show_correct
        self.score_formula = score_formula
        self.score = score

    def to_json(self):
        return {
            "title": self.title,
            "name": "fill-blanks",
            "text": self.text,
            "source": {
                "is_case_sensitive": not self.caseless,
                "components": self.components
            },
            "is_html_enabled": True
        }

    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.text:
            raise ValueError("Question must not be empty.")
        if not self.components:
            raise ValueError("Components must not be empty.")
