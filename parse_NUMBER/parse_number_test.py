import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from step_classes import Step


def test_parse_NUMBER_class():
    text =\
"""Можно задать вопрос, где ответ - число с указанной точностью. Точность пишется после +- после числа.

Чему равно π?

ANSWER: 3.1415 +- 0.01"""
    ans_text = '''Можно задать вопрос, где ответ - число с указанной точностью. Точность пишется после +- после числа.

Чему равно π?
'''
    test = Step.parse(1, "title", text, "NUMBER")

    assert test.text == ans_text

    assert test.answer == 3.1415
    assert test.tolerance == 0.01
    
test_parse_NUMBER_class()