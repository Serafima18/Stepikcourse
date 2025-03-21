import pytest


from parse_number import number, parse_answer, parse_NUMBER

def test_parse_NUMBER():
    text =\
"""Можно задать вопрос, где ответ - число с указанной точностью. Точность пишется после +- после числа.

Чему равно π?

ANSWER: 3.1415 +- 0.01
ANSWER: 3.14"""
    res = parse_NUMBER(text)
    
    assert res["answer"] == [3.1415, 3.14]
    assert res["uncertainty"] == [0.01, 0]
