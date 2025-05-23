import pyparsing as pp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from step_classes import Step


class StepTaskinline(Step):
    """
    Класс для taskinline.
    """

    @classmethod
    def parse(cls, step_id, title, text, step_type='TASKINLINE'):
        score_default = 10
        visible_tests_default = "all"
        checkers = ["text", "std_float_seq"]
        checker_default = checkers[0]

        # Базовые элементы
        section_keyword = pp.oneOf(["CODE", "HEADER", "FOOTER", "TEST", "CONFIG"])
        colon = pp.Suppress(pp.Optional(pp.White()) + pp.Literal(":") + pp.Optional(pp.White()))
        newline = pp.Suppress(pp.LineEnd())
        stringEnd = pp.stringEnd

        # Разделители тестов
        test_delimiter = pp.Suppress(pp.Regex(r"-{4,}"))
        test_end = pp.Suppress(pp.Regex(r"={4,}"))

        # CONFIG с поддержкой параметров
        config_param = pp.oneOf(["score", "visible_tests", "checker", "additional_params"])
        config_value = pp.restOfLine
        config_line = config_param + colon + config_value

        def parse_config(tokens):
            config = {
                "score": "10",
                "visible_tests": "all",
                "checker": "text",
                "additional_params": ""
            }

            for param, value in zip(tokens[1::2], tokens[2::2]):
                if param == "score":
                    config["score"] = value

                elif param == "visible_tests":
                    config["visible_tests"] = value

                elif param == "checker":
                    if value.strip() not in checkers:
                        return {}
                    config["checker"] = value.strip()

                elif param == "additional_params":
                    config["additional_params"] = value

            return config

        config_section = (pp.Literal("CONFIG") + pp.OneOrMore(config_line)
            ).setParseAction(lambda t: {"type": "CONFIG", "data": parse_config(t)})

        # TEST
        test_input = pp.SkipTo(test_delimiter).leaveWhitespace()
        test_output = pp.SkipTo(test_end).leaveWhitespace()

        test_case = (test_input + test_delimiter + 
            test_output + test_end).setParseAction(
            lambda t: {"input": t[0].strip('\n'), "output": t[1].strip('\n')}
        )

        test_section = (pp.Literal("TEST") + 
            pp.OneOrMore(test_case)).setParseAction(
            lambda t: {"type": "TEST", "data": t[1:]})

        # Парсер для других секций
        content = pp.SkipTo(section_keyword | stringEnd)
        other_section = (section_keyword + content).setParseAction(
            lambda t: {"type": t[0], "data": t[1]})

        # Парсер условия задачи
        task_condition = pp.SkipTo(section_keyword)

        # Основной парсер
        task_parser = (
            task_condition("condition") + 
            pp.OneOrMore(
                pp.Group(test_section)("tests") | 
                pp.Group(config_section)("config") | 
                pp.Group(other_section)("other")
            )
        )

        def parse_task_text(text):
            if not task_parser.matches(text):
                print("Ошибка: текст не соответствует формату")
                return {}

            result = task_parser.parseString(text)

            parsed = {
                "condition": result["condition"],
                "CODE": "",
                "HEADER": "",
                "FOOTER": "",
                "TESTS": [],
                "CONFIG": {
                    "score": 10,
                    "visible_tests": "all",
                    "checker": "text",
                    "additional_params": ""
                }
            }

            for section in result[1:]:
                section = section[0]
                if section["type"] == "TEST":
                    parsed["TESTS"].extend(section["data"])
                elif section["type"] == "CONFIG":
                    config = section["data"]

                    parsed["CONFIG"].update({
                        "score": int(config.get("score", score_default)),
                        "visible_tests": (
                            int(config["visible_tests"]) 
                            if "visible_tests" in config and config["visible_tests"].isdigit()
                            else config.get("visible_tests", visible_tests_default)
                        ),
                        "checker": config.get("checker", checker_default),
                        "additional_params": config.get("additional_params", "")
                    })

                elif section["type"] in ["HEADER", "FOOTER", "CODE"]:
                    parsed[section["type"]] = section["data"]

            if not parsed["TESTS"]:
                print("Ошибка: Обязательный блок TEST отсутствует")
                return {}

            return parsed

        result = parse_task_text(text)

        return StepTaskinline(step_id, title, result["condition"],
                              result["TESTS"], result["CODE"], result["HEADER"],
                              result["FOOTER"], result["CONFIG"])

    def __init__(self, step_id, title, text, tests, code=None, header=None,
                 footer=None, config={}):
        super().__init__(step_id, title, text)
        self.tests = tests
        self.code = code
        self.header = header
        self.footer = footer
        self.config = config

    def to_json(self):
        return {
            "name": "taskinline",
            "text": self.text,
            "options": {
                "code_templates": [{
                    "text": self.code
                }],
                "tests": self.tests,
                "header": self.header,
                "footer": self.footer,
                "limits": {
                    "score": self.config["score"]
                },
                "visible_tests": self.config["visible_tests"],
                "checker": self.config["checker"],
                "additional_params": self.config["additional_params"]
            }
    }


    def validate(self):
        """
        Проверяет, что все необходимые атрибуты заданы корректно.
        """
        if not self.text:
            raise ValueError("Condition must not be empty.")
        if not self.tests:
            raise ValueError("Tests must not be empty.")
        if self.code and not isinstance(self.code, str):
            raise ValueError("Code must be a string if provided.")
        if self.header and not isinstance(self.header, str):
            raise ValueError("Header must be a string if provided.")
        if self.footer and not isinstance(self.footer, str):
            raise ValueError("Footer must be a string if provided.")
