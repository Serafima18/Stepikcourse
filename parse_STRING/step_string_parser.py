import requests
import pyparsing as pp
from step_classes import StepString


class StepStringParser:
    def __init__(self, information):
        self.text = information

    def parse_step_string(self):
        token = pp.Word(pp.alphanums)
        step_id = pp.Word(pp.alphanums)
        position = pp.Word(pp.alphanums)
        step_text = pp.QuotedString('"') | pp.OneOrMore(pp.Word(pp.alphas + pp.alphanums + ' '))

        step_string_parser = pp.Group(
            pp.Suppress("StepString(") + token + pp.Suppress(",") + step_id + pp.Suppress(",") + position + pp.Suppress(
                ",") + step_text + pp.Suppress(")"))

        result = step_string_parser.parseString(self.text)
        return {
            'token': result[0],
            'id': result[1],
            'position': result[2],
            'text': ' '.join(result[3:])
        }

    def parse_to_md(self):
        inf = self.parse_step_string()
        md_ans = f"**Parsed StepString Information**\n"
        md_ans += f"- **Token**: {inf['token']}\n"
        md_ans += f"- **ID**: {inf['id']}\n"
        md_ans += f"- **Position**: {inf['position']}\n"
        md_ans += f"- **Text**: {inf['text']}"
        return md_ans


def test_parser():
    session = requests.Session()
    token = 'token'
    step = StepString(token, 1, 0, session, 'some text')

    parser = StepStringParser(step)  # здесь должно быть step.get_data()
    parsed_data = parser.parse_to_md()

    print(parsed_data)


test_parser()
