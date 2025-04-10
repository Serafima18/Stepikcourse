from step_classes import Step


def test_parsing_quiz1():
    text = \
'''
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
    step_test = Step(1, "title")
    question, possible_answers, shuffle, answer = step_test.parse(text, "QUIZ")
    assert question == \
'''Отметьте правильные ответы. SHUFFLE - перемешивать ответы при очередном прохождении теста.
По умолчанию они перемешиваются. Отключается перемешивание установкой опции в значение false (без учета регистра).

Множественный выбор - пишем буквы в ответе через запятую. Пробелы игнорируются.
'''
    assert answer == [['A', 'D', 'C']]
    assert possible_answers == \
           {
               'A': 'Это правильный ответ.',
               'B': 'Нет.',
               'C': 'Тоже хорошо.',
               'D': 'Еще один правильный.'
           }
    assert not shuffle


def test_parsing_quiz2():
    text = \
'''
TEXTBEGIN
Если текст вопроса может выглядеть как вариант ответа, то есть начаться с а) или a., то стоит явно обозначить начало и 
конец вопроса с помощью TEXTBEGIN и TEXTEND.

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
    step_test = Step(1, "title")
    question, possible_answers, shuffle, answer = step_test.parse(text, "QUIZ")
    assert question == \
'''Если текст вопроса может выглядеть как вариант ответа, то есть начаться с а) или a., то стоит явно обозначить начало и 
конец вопроса с помощью TEXTBEGIN и TEXTEND.

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
'''
    assert answer == [['A', 'C']]
    assert possible_answers == \
           {
               'A': "square(100, 'red') нарисует красный квадрат размером 100",
               'B': "square(100) нарисует красный квадрат размером 100",
               'C': "square(100) нарисует синий квадрат размером 100"
           }
    assert shuffle
