from step_classes import Step


def test_parsing_string1():
    text = \
'''
Какой ваш любимый цвет?
ANSWER: Синий
ANSWER: Красный
'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.question == "Какой ваш любимый цвет?"
    assert step_test.answer == ["синий", "красный"]


def test_parsing_string2():
    text = \
'''
Попросим студента написать "MIPT". Напишите "MIPT".

ANSWER: MIPT
'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.question == 'Попросим студента написать "MIPT". Напишите "MIPT".\n'
    assert step_test.answer == ["mipt"]


def test_parsing_string3():
    text = \
'''
Попросим студента написать "Я учусь в МФТИ". Напишите  "Я учусь в МФТИ".

Много строк в условии.

ANSWER:  Я учусь в МФТИ

'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.question == \
'''Попросим студента написать "Я учусь в МФТИ". Напишите  "Я учусь в МФТИ".

Много строк в условии.
'''
    assert step_test.answer == ["я учусь в мфти"]
