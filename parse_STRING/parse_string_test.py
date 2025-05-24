from step_classes import Step
from markdown import markdown


def test_parsing_string1():
    text = '''
Какой ваш любимый цвет?
ANSWER: Синий
'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.text == markdown("Какой ваш любимый цвет?").replace("\n", "<br>")
    assert step_test.answer == "Синий"


def test_parsing_string2():
    text = '''
Попросим студента написать "MIPT". Напишите "MIPT".

ANSWER: MIPT
'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.text == markdown('Попросим студента написать "MIPT". Напишите "MIPT".\n').replace("\n", "<br>")
    assert step_test.answer == "MIPT"


def test_parsing_string3():
    text = '''
Попросим студента написать "Я учусь в МФТИ". Напишите  "Я учусь в МФТИ".

Много строк в условии.

ANSWER:  Я учусь в МФТИ

'''
    step_test = Step.parse(1, 'title', text, "STRING")
    assert step_test.text == markdown('''Попросим студента написать "Я учусь в МФТИ". Напишите  "Я учусь в МФТИ".

Много строк в условии.
''').replace("\n", "<br>")
    assert step_test.answer == "Я учусь в МФТИ"
