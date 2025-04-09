'''
example 

module_name = pp.Word(pp.alphas + '_')
full_module_name = (module_name + pp.ZeroOrMore(pp.Suppress('.') + module_name)) ('modules')  # дали имя modules
import_as = (pp.Optional(pp.Suppress('as') + module_name))('import_as')                       # дали имя import_as
parse_module = (pp.Suppress('import') + full_module_name + import_as).setParseAction(lambda t: {'import': t.modules.asList(), 'as': t.import_as.asList()[0]})
parse_module.parseString(text).asList()[0]
'''


import pyparsing as pp


# lesson_id
lesson_id_key = pp.Suppress('lesson_id:')
lesson_id_value = pp.Word(pp.nums) ('lesson_id')
parse_lesson_id = (lesson_id_key + lesson_id_value)

# lang
lang_key = pp.Suppress('lang:')
lang_value = pp.Word(pp.alphas) ('lang')
parse_lang = (lang_key + lang_value)

# h2
h2_prefix = pp.Suppress('##')
h2_type = pp.Optional(pp.Suppress('[') + pp.Word(pp.alphas)('type') + pp.Suppress(']'), default='TEXT') ('type')
h2_title = pp.restOfLine ('title')
parse_h2 = (h2_prefix + h2_type + h2_title)



text = """lesson_id: 123456
lang: qwerty
## [SKIP] title 1
first
second
## title 2
first again
second again
"""

lines = [line for line in text.splitlines()]
results = []

lesson_id_result = parse_lesson_id.parseString(lines[0])
lang_result = parse_lang.parseString(lines[1])

results.append({'lesson_id': lesson_id_result.lesson_id, 'lang': lang_result.lang})

current_h2 = None
current_text = []

for line in lines[2:]:
    if parse_h2.matches(line):
        h2_current = parse_h2.parseString(line)
        if current_h2:
            results.append({'h2': current_h2, 'text': "\n".join(current_text)})
            current_text = []

        current_h2 = {'type': h2_current.type.asList()[0], 'title': h2_current.title}
    else:
        current_text.append(line)

if current_h2:
    results.append({'h2': current_h2, 'text': "\n".join(current_text)})


for result in results:
    print(result)
