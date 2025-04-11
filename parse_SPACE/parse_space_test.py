from step_classes import Step


def test_parsing_space1():
    text = \
'''
Задание заполнить пробелы

TEXTBEGIN
Заполни вот этот ___ пробел чем_нибудь.
И вот этот ___ тоже
TEXTEND

ANSWER: Red, Blue
'''
    step_test = Step(1, "title")
    question, txt_space, space_number, answer = step_test.parse(text, "SPACE")
    assert question == \
'''Задание заполнить пробелы

'''
    assert answer == [
        {
            1: 'Red',
            2: 'Blue'
        }
    ]

    assert txt_space == \
'''Заполни вот этот ___ пробел чем_нибудь.
И вот этот ___ тоже'''

    assert space_number == 2
