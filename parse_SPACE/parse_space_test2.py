from step_classes import Step
from markdown import markdown

text = '''
Some question
SPACETEXT
First space ___[1;2;3] second space ___[1;@2;3]
Third space ___[4;5]
CONFIG
CASELESS: true
SHOW_CORRECT: true
SCORE_FORMULA: True
SCORE: 7
'''

step_test = Step.parse(1, 'title', text, 'SPACE')


def test_parse_space2_question():
    assert step_test.text == markdown('Some question').replace("\n", "<br>")


def test_parse_space2_components():
    assert step_test.components == [
        {
            "type": "text",
            "content": markdown("First space ").replace("\n", "<br>")
        },
        {
            "type": "input",
            "correct": ["1", "2", "3"]
        },
        {
            "type": "text",
            "content": markdown(" second space ").replace("\n", "<br>")
        },
        {
            "type": "select",
            "options": ["1", "2", "3"],
            "correct": ["2"]
        },
        {
            "type": "text",
            "content": markdown("Third space ").replace("\n", "<br>")
        },
        {
            "type": "input",
            "correct": ["4", "5"]
        }
    ]


def test_parse_space2_caseless():
    assert step_test.caseless


def test_parse_space2_show_correct():
    assert step_test.show_correct


def test_parse_space2_score_formula():
    assert step_test.score_formula


def test_parse_space2_score():
    assert step_test.score == 7
