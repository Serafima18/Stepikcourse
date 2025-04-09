from re        import VERBOSE
import pyparsing as pp


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
    # print(f'{t=}')
    if t.float1 or t.float2 or t.float3 : return [float(t[0])]
    else                                : return [int(t[0])  ]

number.setParseAction(convert_number)
#number.searchString('10')


uncertainty = pp.Suppress("+-") + number

parse_answer = (
    pp.Suppress("ANSWER:")
    + number ("value")
    + pp.Optional(pp.Suppress("+-") + number ("uncertainty")) 
)

def parse_NUMBER(text):
    lines = [line for line in text.splitlines()]
    results = {
        "question": [],  # Текст вопроса
        "answer": [],  # Ответы
        "uncertainty": [],  # Погрешности
    }

    for line in lines:
        if not results["answer"]:
            if not parse_answer.matches(line):
                results["question"].append(line)
        
        if parse_answer.matches(line):
            answer_result = parse_answer.parseString(line)

            results["answer"].append(answer_result.value)
            if answer_result.uncertainty:
                results["uncertainty"].append(answer_result.uncertainty)
            else:
                results["uncertainty"].append(0)
    
    return results


text =\
"""Можно задать вопрос, где ответ - число с указанной точностью. Точность пишется после +- после числа.

Чему равно π?

ANSWER: 3.1415 +- 0.01
ANSWER: 3.14"""

res = parse_NUMBER(text)
print(res["answer"], res["uncertainty"])