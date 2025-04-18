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
    step_test = Step.parse(1, 'title', text, "SPACE")
    assert step_test.question == \
'''Задание заполнить пробелы

'''
    assert step_test.answer == [
        {
            1: 'Red',
            2: 'Blue'
        }
    ]

    assert step_test.txt_space == \
'''Заполни вот этот ___ пробел чем_нибудь.
И вот этот ___ тоже'''

    assert step_test.space_number == 2
