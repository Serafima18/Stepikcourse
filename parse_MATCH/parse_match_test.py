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
====

'''

    step_test = Step.parse(1, 'title', text, 'MATCHING')

    assert step_test.question == 'Какой-то вопрос???'
    assert step_test.pairs == [
        {
            'first': 'строка 1',
            'second': 'сопоставление1'
        },

        {
            'first': 'цвет неба',
            'second': 'голубой'
        },

        {
            'first': 'цвет арбуза',
            'second': 'красный'
        }
    ]


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
====

'''
    step_test = Step.parse(1, 'title', text, 'MATCHING')

    assert step_test.question == 'Question???\nQuestion question'

    assert step_test.pairs == [
        {
            'first': 'str 1',
            'second': 'match1'
        },

        {
            'first': 'str str str\nstr str str',
            'second': 'match2'
        },

        {
            'first': 'str 3',
            'second': 'match3\nmatch3'
        }
    ]
