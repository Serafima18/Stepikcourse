from step_classes import Step, StepString


def test_parsing():
    step_test = Step(1, "")
    ans = {"data": ""}
    assert step_test.parse_step() == ans


def test_parsing_string():
    step_test = StepString(1, "Хочу задать вопрос", "Какой ваш любимый цвет?", ["Синий", "Красный"])
    right_ans = {"question": "Какой ваш любимый цвет?", "answer": ["синий", "красный"]}
    assert right_ans == step_test.parse_step()
