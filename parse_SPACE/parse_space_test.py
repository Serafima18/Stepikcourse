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
    step_space_test = step_test.parse(text, "SPACE")
    assert step_space_test.question == \
'''Задание заполнить пробелы

'''
    assert step_space_test.answer == [
        {
            1: 'Red',
            2: 'Blue'
        }
    ]

    assert step_space_test.txt_space == \
'''Заполни вот этот ___ пробел чем_нибудь.
И вот этот ___ тоже'''

    assert step_space_test.space_number == 2
