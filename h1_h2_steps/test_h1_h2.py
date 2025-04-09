import pytest

from h1_h2_steps import parse_h1, parse_lesson_id, parse_lang, parse_h2, parse_text


@pytest.mark.parametrize('text,lesson_title', [
    ('# title of lesson', 'title of lesson'),
    ('  # title of lesson', ''),
    ('my code # title', ''),
 ])
def test_h1_space(text, lesson_title):
    """Проверка пробела перед # шаблона parse_h1"""
    if parse_h1.matches(text):
        result = parse_h1.parseString(text)
        result = result.lesson_title
    else:
         result = ''
    assert result == lesson_title


@pytest.mark.parametrize('text,lang', [
    ('lang: cpp ', 'cpp'),
    ('lang: python310 ', 'python310'),
    ('lang: c_valgrind', 'c_valgrind'),
    ('lang: python3_12 ', 'python3_12')
])
def test_lang(text, lang):
    """Проверка шаблона parse_lang"""
    result = parse_lang.parseString(text)
    assert result.lang == lang


@pytest.mark.parametrize('text,lang', [
    ('lang: cpp ', 'cpp'),
    ('lang:cpp', 'cpp'),
    ('    lang:cpp', 'cpp'),
    ('lang : cpp ', 'cpp'),
    ('  lang :cpp ', 'cpp'),
 ])
def test_lang_space(text, lang):
    """Проверка пробела перед : шаблона parse_lang"""
    result = parse_lang.parseString(text)
    assert result.lang == lang


'## QUIZ my quiz'
'это код ## и комментарий'


@pytest.mark.parametrize('text,header', [
    ('## QUIZ my quiz', 'my quiz'),
    ('  ## QUIZ my quiz', ''),
    ('my code ## QUIZ my quiz', ''),
 ])
def test_h2_space(text, header):
    """Проверка пробела перед ## шаблона parse_h2"""
    if parse_h2.matches(text):
        result = parse_h2.parseString(text)
        result = result.header
    else:
         result = ''
    assert result == header


@pytest.mark.parametrize('text,type,skip', [
    ('## QUIZ my quiz', 'QUIZ', 'False'),
    ('## QUIZ SKIP my quiz', 'QUIZ', 'True'),
    ('## SKIP QUIZ my quiz', 'QUIZ', 'True'),
    ('## SKIP my quiz', 'TEXT', 'True'),
    ('## QUIZ my quiz', 'QUIZ', 'False'),
    ('## my quiz', 'TEXT', 'False'),
 ])
def test_h2_type_skip(text, type, skip):
    """Проверка SKIP+TYPE шаблона parse_h2"""
    result = parse_h2.parseString(text)
    result = {'type': result.type,
                'skip': 'True' if result.skip else 'False', 
                'header': result.header}

    result_type = result['type']
    result_skip = result['skip']

    assert result_type == type
    assert result_skip == skip


def test_to_steps():
    text = \
"""# title
lesson_id: 123456



lang: qwerty





## SKIP VIDEO title 1
first

second
## TEXT SKIP title 2

first again
second again"""

    result = parse_text(text)

    assert result[0]['lesson_title'] == 'title'

    assert result[1]['lesson_id'] == '123456'
    assert result[2]['lang'] == 'qwerty'


    step = result[3]

    h2 = step['h2']
    assert h2['header'] == 'title 1'
    assert h2['type'] == 'VIDEO'
    assert h2['skip'] == 'True'
    assert step['text'] == 'first\n\nsecond'


    step = result[4]

    h2 = step['h2']
    assert h2['header'] == 'title 2'
    assert h2['type'] == 'TEXT'
    assert h2['skip'] == 'True'
    assert step['text'] == '\nfirst again\nsecond again'
