from parse_string import parse_str


def test_parsing_string():
    text = \
"""Хочу задать вопрос

Какой ваш любимый цвет?

ANSWER: Синий
"""
    right_ans = {}

    right_ans["question"] = "Хочу задать вопросКакой ваш любимый цвет?"
    right_ans["answer"] = ["Синий"]
    assert right_ans == parse_str(text)
