from step_classes import Step
from markdown import markdown

text = '''
Тут будет текст вопроса на несколько строк.
SPACETEXT
2 + 2 = ____[4] это ввод, указываем правильный ответ
2 + 3 = ____[5;пять] тоже ввод, но вариантов правильного ответа несколько
2 + 4 = ____[4;5;@6;7;@шесть;пять] это выбор с указанием правильных выборов
CONFIG
CASELESS: true
SHOW_CORRECT: true
SCORE_FORMULA: True
SCORE: 5
'''

step_test = Step.parse(1, 'title', text, "SPACE")


def test_parsing_space1_question():
    assert step_test.text == markdown('Тут будет текст вопроса на несколько строк.')


def test_parsing_space1_answer():
    assert step_test.answer == {
        'space with choice': {
            3: {
                'right ans': ['6', 'шесть'],
                'all ans': ['4', '5', '6', '7', 'шесть', 'пять']
            }
        },

        'space without': {
            1: ['4'],
            2: ['5', 'пять']
        }
    }


def test_parsing_space1_txt_space():
    assert step_test.txt_space == '''2 + 2 = ____ это ввод, указываем правильный ответ
2 + 3 = ____ тоже ввод, но вариантов правильного ответа несколько
2 + 4 = ____ это выбор с указанием правильных выборов'''


def test_parsing_space1_space_number():
    assert step_test.space_number == 3


def test_parsing_space1_caseless():
    assert step_test.caseless


def test_parsing_space1_show_correct():
    assert step_test.show_correct


def test_parsing_space1_score_formula():
    assert step_test.score_formula


def test_parsing_space1_score():
    assert step_test.score == 5
