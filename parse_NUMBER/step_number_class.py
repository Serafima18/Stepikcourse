import pyparsing  as pp
from re           import VERBOSE
from step_classes import Step

class StepNumber(Step):
    """
    Класс для задач Number.
    """

    @classmethod
    def parse(cls, step_id, title, text, step_type='NUMBER'):
        number = pp.Regex(r"""
                [+-]?                           # optional sign
                (
                    (?:\d+(?P<float1>\.\d*)?)   # match 2 or 2.02
                |                             # or
                    (?P<float2>\.\d+)           # match .02
                )
                (?P<float3>[Ee][+-]?\d+)?      # optional exponent
                """, flags=VERBOSE
                )


        def convert_number(t: pp.ParseResults):
            """Convert a string matching a number to a python number"""
            if t.float1 or t.float2 or t.float3 : return [float(t[0])]
            else                                : return [int(t[0])  ]

        number.setParseAction(convert_number)


        #tolerance = pp.Suppress("+-") + number
        
        parse_answer = (
            pp.Suppress("ANSWER:")
            + number ("value")
            + pp.Optional(pp.Suppress("+-") + number ("tolerance")) 
        )


        lines = [line for line in text.splitlines()]
        results = {
            "text": str,  # Текст вопроса
            "answer": float,  # Ответы
            "tolerance": float,  # Погрешности
        }

        for line in lines:
            if not results["answer"]:
                if not parse_answer.matches(line):
                    if results["text"]:
                        results[text] += "\n"
                    results["text"] += line
            
            if parse_answer.matches(line):
                answer_result = parse_answer.parseString(line)

                results["answer"] = answer_result.value
                if answer_result.tolerance:
                    results["tolerance"] = answer_result.tolerance
                else:
                    results["tolerance"] = 0

                #results["answer"].append(answer_result.value)
                #if answer_result.tolerance:
                #    results["tolerance"].append(answer_result.tolerance)
                #else:
                #    results["tolerance"].append(0)

        return StepNumber(step_id, title, text, results["answer"], results["tolerance"])

    def __init__(self, step_id: int, title: str, text: str, answer: float, tolerance: float = 0):
        super().__init__(step_id, title, text)
        self.text = text
        self.answer = answer
        self.tolerance = tolerance

    def to_json(self) -> dict:
        return {
            "name": "number",
            "text": self.text,
            "answer": f"{self.answer} ± {self.tolerance}",
            "is_html_enabled": True
        }

    def validate(self) -> None:
        if self.answer is None:
            raise ValueError("Answer must not be None.")
        if self.tolerance < 0:
            raise ValueError("Tolerance must not be negative.")
