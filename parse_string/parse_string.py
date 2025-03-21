import pyparsing as pp
from step_classes import Step, StepString


def parse_step(self):
    pass


Step.parse_step = parse_step


def parse_str(self):
    text = str(self)
    lines = [line for line in text.splitlines()]
    results = {
        "question": "",
        "answer": [],
    }

    letters = "абвгдежзийклмнопрстуфхцчшщъыьэюя ',-.!?()[]{}\""
    parse_answer = pp.Suppress("ANSWER:") + pp.Word(pp.alphas + pp.nums + letters + letters.upper())

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if not results["answer"]:
            if not parse_answer.matches(line):
                results["question"] += line

        if parse_answer.matches(line):
            answer_result = parse_answer.parseString(line)
            results["answer"].append(" ".join(answer_result))

    return results


StepString.parse_step = parse_str
