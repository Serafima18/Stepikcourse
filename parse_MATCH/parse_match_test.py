from step_classes import Step


def test_parse_match1():
    text = '''
Какой-то вопрос???
MATCH
строка 1
——
сопоставление1
====
цвет неба
——
голубой
====
цвет арбуза
——
красный

ANSWER: 1-1,2-2,3-3
'''

    step_test = Step.parse(1, 'title', text, 'MATCH')

    assert step_test.question == 'Какой-то вопрос???'
    assert step_test.ln_left == [
        'строка 1',
        'цвет неба',
        'цвет арбуза'
    ]

    assert step_test.ln_right == [
        'сопоставление1',
        'голубой',
        'красный'
    ]

    assert step_test.answer == {
        1: 1,
        2: 2,
        3: 3
    }


def test_parse_match2():
    text = '''
Question???
Question question
MATCH
str 1
——
match1
====
str str str
str str str
——
match2
====
str 3
——
match3
match3

ANSWER: 1-1,2-2,3-3
'''
    step_test = Step.parse(1, 'title', text, 'MATCH')

    assert step_test.question == 'Question???\nQuestion question'

    assert step_test.ln_left == [
        'str 1',
        'str str str\nstr str str',
        'str 3'
    ]

    assert step_test.ln_right == [
        'match1',
        'match2',
        'match3\nmatch3'
    ]

    assert step_test.answer == {
        1: 1,
        2: 2,
        3: 3
    }