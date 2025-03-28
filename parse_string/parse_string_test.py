from step_classes import Step, StepString


def test_parsing():
    step_test = Step(1, "")
    ans = {"data": ""}
    assert step_test.parse_step() == ans


def test_parsing_string():
    text = \
'''
Какой ваш любимый цвет?
ANSWER: Синий
ANSWER: Красный
'''
    step_test = StepString(1, "Хочу задать вопрос", text)
    step_test.parse_step()
    assert step_test.question == "Какой ваш любимый цвет?"
    assert step_test.answer == ["синий", "красный"]
