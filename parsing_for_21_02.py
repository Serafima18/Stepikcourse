import pyparsing as pp

# Определение грамматики
identifier = pp.Word(pp.alphas + '_', pp.alphanums + '_')
equals = pp.Suppress('=')
string_value = pp.Suppress('"') + pp.Word(pp.alphanums + '_-') + pp.Suppress('"')

# Правила для заголовков
h2 = pp.Literal('h2') + pp.Group(pp.restOfLine)
header = pp.Group(h2)
header.setParseAction(lambda t: ('h2', t[0][1]))

# Переменные
variable = pp.Group(identifier + equals + string_value)
variables = pp.OneOrMore(variable)

# Полная структура
file_structure = pp.OneOrMore(header | variables)

# Пример файла
input_text = """
lesson_id = "12345"
lang = "ru"
h2 Заголовок второго уровня
"""

result = file_structure.parseString(input_text)

for item in result:
    if isinstance(item, tuple):
        print(f"Заголовок - Тип: {item[0]}, Текст: {str(item[1]).strip()}")
    else:
        print(f"Переменная - Имя: {item[0]}, Значение: {item[1]}")
