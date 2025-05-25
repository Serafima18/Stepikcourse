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
    assert step_test.text == markdown('Тут будет текст вопроса на несколько строк.').replace("\n", "<br>")


def test_parsing_space1_components():
    assert step_test.components == [
        {
            "type": "text",
            "content": markdown("2 + 2 = ").replace("\n", "<br>")
        },
        {
            "type": "input",
            "correct": ["4"]
        },
        {
            "type": "text",
            "content": markdown(''' это ввод, указываем правильный ответ
2 + 3 = ''').replace("\n", "<br>")
        },
        {
            "type": "input",
            "correct": ["5", "пять"]
        },
        {
            "type": "text",
            "content": markdown(''' тоже ввод, но вариантов правильного ответа несколько
2 + 4 = ''').replace("\n", "<br>")
        },
        {
            "type": "select",
            "options": ["4", "5", "6", "7", "шесть", "пять"],
            "correct": ["6", "шесть"]
        },
        {
            "type": "text",
            "content": markdown(" это выбор с указанием правильных выборов").replace("\n", "<br>")
        }
    ]


def test_parsing_space1_caseless():
    assert step_test.caseless


def test_parsing_space1_show_correct():
    assert step_test.show_correct


def test_parsing_space1_score_formula():
    assert step_test.score_formula


def test_parsing_space1_score():
    assert step_test.score == 5
