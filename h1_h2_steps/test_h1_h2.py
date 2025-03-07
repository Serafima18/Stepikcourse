import pytest

from h1_h2_steps import parse_lang, parse_lesson_id, parse_text, parse_h2


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


    h1 = result[0]

    h1['lesson_title'] =='title'


    lesson_id_lang = result[1]

    lesson_id_lang['lesson_id'] == '123456'
    lesson_id_lang['lang'] == 'qwerty'


    step = result[2]

    h2 = step['h2']
    assert h2['header'] == 'title 1'
    assert h2['type'] == 'VIDEO'
    assert h2['skip'] == 'True'
    assert step['text'] == 'first\nsecond'


    step = result[3]

    h2 = step['h2']
    assert h2['header'] == 'title 2'
    assert h2['type'] == 'TEXT'
    assert h2['skip'] == 'True'
    assert step['text'] == 'first again\nsecond again'
