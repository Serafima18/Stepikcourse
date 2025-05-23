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
''')
    assert step_test.possible_answers == [
        {
            "text": "Это правильный ответ.",
            "is_correct": True
        },
        {
            "text": "Нет.",
            "is_correct": False,
        },
        {
            "text": "Тоже хорошо.",
            "is_correct": True,
        },
        {
            "text": "Еще один правильный.",
            "is_correct": True
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
''')
    assert step_test.possible_answers == [
        {
            "text": "square(100, 'red') нарисует красный квадрат размером 100",
            "is_correct": True
        },
        {
            "text": "square(100) нарисует красный квадрат размером 100",
            "is_correct": False
        },
        {
            "text": "square(100) нарисует синий квадрат размером 100",
            "is_correct": True
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
''')
    assert step_test.possible_answers == {
               'ответ 1': False,
               '''В ответе может быть любое форматирование, даже код. В коде знаки < и > должны быть обрамлены пробелами с двух сторон (баг на stepik).
if 2 < 3:
    print('Hello, world!')''': False,
               'answer 2 правильный': True,
               '''
x = 'Ответ только из блока кода, блок кода надо написать с новой строки'
print(x)''': False
           }
    assert step_test.shuffle
