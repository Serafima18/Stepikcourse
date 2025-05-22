from step_classes import Step

text = '''
Some question
SPACETEXT
First space ___[1;2;3] second space ___[1;@2;3@4;@35@4]
Third space ___[4;5@7]
CONFIG
CASELESS: true
SHOW_CORRECT: true
SCORE_FORMULA: True
SCORE: 3
'''

step_test = Step.parse(1, 'title', text, 'SPACE')


def test_parse_space2_question():
    assert step_test.text == 'Some question'


def test_parse_space2_txt_space():
    assert step_test.txt_space == '''First space ___ second space ___
Third space ___'''


def test_parse_space2_space_number():
    assert step_test.space_number == 3


def test_parse_space2_answer():
    assert step_test.answer == {
        'space with choice': {
            2: {
                'right ans': ['2', '35@4'],
                'all ans': ['1', '2', '3@4', '35@4']
            }
        },

        'space without': {
            1: ['1', '2', '3'],
            3: ['4', '5@7']
        }
    }


def test_parse_space2_caseless():
    assert step_test.caseless


def test_parse_space2_show_correct():
    assert step_test.show_correct


def test_parse_space2_score_formula():
    assert step_test.score_formula


def test_parse_space2_score():
    assert step_test.score == 3
