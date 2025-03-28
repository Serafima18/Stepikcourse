import pyparsing as pp
from step_classes import Step, StepString


def parse_step(self):
    return {"data": ""}


def get_txt(self):
    txt = self.question
    for ans in self.answer:
        txt += '\nANSWER: ' + ans
    return txt


def parse_str(self):
    text = self.get_txt()
    lines = [line for line in text.splitlines()]
    results = {
        "question": "",
        "answer": [],
    }

    parse_answer = pp.Suppress("ANSWER:") + pp.SkipTo(pp.LineEnd())

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if not results["answer"]:
            if not parse_answer.matches(line):
                results["question"] += line

        if parse_answer.matches(line):
            answer_result = parse_answer.parseString(line)
            results["answer"].append(" ".join(answer_result).strip().lower())

    return results


def add_methods():
    Step.parse_step = parse_step
    StepString.get_txt = get_txt
    StepString.parse_step = parse_str
