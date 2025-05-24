from step_classes import Step
from markdown import markdown


def test_parsing_quiz1():
    text = '''
Отметьте правильные ответы. SHUFFLE - перемешивать ответы при очередном прохождении теста.
По умолчанию они перемешиваются. Отключается перемешивание установкой опции в значение false (без учета регистра).

Множественный выбор - пишем буквы в ответе через запятую. Пробелы игнорируются.

A. Это правильный ответ.
B. Нет.
C. Тоже хорошо.
D. Еще один правильный.

SHUFFLE: False 
ANSWER: A, D, C
'''
    step_test = Step.parse(1, 'title', text, "QUIZ")
    assert step_test.text == \
markdown('''Отметьте правильные ответы. SHUFFLE - перемешивать ответы при очередном прохождении теста.
По умолчанию они перемешиваются. Отключается перемешивание установкой опции в значение false (без учета регистра).

Множественный выбор - пишем буквы в ответе через запятую. Пробелы игнорируются.
''').replace("\n", "<br>")
    assert step_test.possible_answers == [
        {
            "text": markdown("Это правильный ответ.").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        },
        {
            "text": markdown("Нет.").replace("\n", "<br>"),
            "is_correct": False,
            "feedback": "Wrong"
        },
        {
            "text": markdown("Тоже хорошо.").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        },
        {
            "text": markdown("Еще один правильный.").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        }
    ]
    assert not step_test.shuffle


def test_parsing_quiz2():
    text = '''
TEXTBEGIN
Если текст вопроса может выглядеть как вариант ответа, то есть начаться с а) или a.,
то стоит явно обозначить начало и конец вопроса с помощью TEXTBEGIN и TEXTEND.

Для черепахи написали функцию

def square(size, col='blue'):
    # рисовать квадрат со стороной size цветом col
    t.color(col)    # установили цвет col
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
Отметьте правильные предложения.
TEXTEND
A. square(100, 'red') нарисует красный квадрат размером 100

B. square(100) нарисует красный квадрат размером 100

C. square(100) нарисует синий квадрат размером 100

ANSWER: A,C
'''
    step_test = Step.parse(1, 'title', text, "QUIZ")
    assert step_test.text == markdown('''Если текст вопроса может выглядеть как вариант ответа, то есть начаться с а) или a.,
то стоит явно обозначить начало и конец вопроса с помощью TEXTBEGIN и TEXTEND.

Для черепахи написали функцию

def square(size, col='blue'):
    # рисовать квадрат со стороной size цветом col
    t.color(col)    # установили цвет col
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
    t.fd(size)
    t.lt(90)
Отметьте правильные предложения.
''').replace("\n", "<br>")
    assert step_test.possible_answers == [
        {
            "text": markdown("square(100, 'red') нарисует красный квадрат размером 100").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        },
        {
            "text": markdown("square(100) нарисует красный квадрат размером 100").replace("\n", "<br>"),
            "is_correct": False,
            "feedback": "Wrong"
        },
        {
            "text": markdown("square(100) нарисует синий квадрат размером 100").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        }
    ]
    assert step_test.shuffle


def test_parsing_quiz3():
    text = '''
Это вопрос в формате AIKEN. SHUFFLE - перемешивать ответы при очередном прохождении теста.
По умолчанию они перемешиваются. Отключается перемешивание установкой опции в значение false (без учета регистра).

A) ответ 1
B) В ответе может быть любое форматирование, даже код. В коде знаки < и > должны быть обрамлены пробелами с двух сторон (баг на stepik).

if 2 < 3:
    print('Hello, world!')
C) answer 2 правильный
D)

x = 'Ответ только из блока кода, блок кода надо написать с новой строки'
print(x)
ANSWER: C
'''
    step_test = Step.parse(1, 'title', text, "QUIZ")
    assert step_test.text == \
markdown('''Это вопрос в формате AIKEN. SHUFFLE - перемешивать ответы при очередном прохождении теста.
По умолчанию они перемешиваются. Отключается перемешивание установкой опции в значение false (без учета регистра).
''').replace("\n", "<br>")
    assert step_test.possible_answers == [
        {
            "text": markdown("ответ 1").replace("\n", "<br>"),
            "is_correct": False,
            "feedback": "Wrong"
        },
        {
            "text": \
markdown('''В ответе может быть любое форматирование, даже код. В коде знаки < и > должны быть обрамлены пробелами с двух сторон (баг на stepik).

if 2 < 3:
    print('Hello, world!')''').replace("\n", "<br>"),
            "is_correct": False,
            "feedback": "Wrong"
        },
        {
            "text": markdown("answer 2 правильный").replace("\n", "<br>"),
            "is_correct": True,
            "feedback": "Right"
        },
        {
            "text": markdown('''

x = 'Ответ только из блока кода, блок кода надо написать с новой строки'
print(x)''').replace("\n", "<br>"),
            "is_correct": False,
            "feedback": "Wrong"
        }
    ]
    assert step_test.shuffle
