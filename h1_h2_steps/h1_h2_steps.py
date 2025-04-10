import pyparsing as pp

# h1
parse_h1 = pp.AtLineStart(pp.Keyword('#')) + pp.White() + (pp.restOfLine()) ('lesson_title')

# lesson_id
lesson_id_key = pp.Suppress('lesson_id' + pp.Optional(pp.White()) + ':')
lesson_id_value = pp.Word(pp.nums) ('lesson_id')
parse_lesson_id = (lesson_id_key + lesson_id_value)

# lang
lang_key = pp.Suppress('lang' + pp.Optional(pp.White()) + ':')
lang_value = pp.Word(pp.alphanums + '_') ('lang')
parse_lang = (lang_key + lang_value)

# h2
skip = pp.Literal("SKIP") ("skip")
h2_start = pp.Literal("##")

task_types = ["TEXT", "PROBLEM", "QUIZ", "NUMBER", "STRING", "VIDEO", "TASK", "TASKINLINE"]
task_type = pp.oneOf(task_types) ("type")

header = pp.restOfLine ("header")

parse_h2 = pp.AtLineStart(h2_start) + pp.Optional(skip) + pp.Optional(task_type, default="TEXT")\
             + pp.Optional(skip) + pp.Optional(pp.White()) + header


def parse_text(text):
    lines = [line for line in text.splitlines()]
    results = []
    
    current_h2 = None
    current_text = []

    for line in lines:
        if parse_h1.matches(line):
            lesson_title_result = parse_h1.parseString(line)
            results.append({'lesson_title': lesson_title_result.lesson_title})

            continue

        elif len(results) < 0:
            continue


        if parse_lesson_id.matches(line):
            lesson_id_result = parse_lesson_id.parseString(line)
            results.append({'lesson_id': lesson_id_result.lesson_id})
            
            continue

        elif len(results) < 1:
            continue


        if parse_lang.matches(line):
            lang_result = parse_lang.parseString(line)
            results.append({'lang': lang_result.lang})
            
            continue

        elif len(results) < 2:
            continue


        if parse_h2.matches(line):
            h2_current = parse_h2.parseString(line)
            if current_h2:
                results.append({'h2': current_h2, 'text': "\n".join(current_text)})
                current_text = []

            current_h2 = {'type': h2_current.type,
                          'skip': 'True' if h2_current.skip else 'False', 
                          'header': h2_current.header}
        elif current_h2:
            current_text.append(line)

    if current_h2:
        results.append({'h2': current_h2, 'text': "\n".join(current_text)})


    for result in results:
        print(result, '\n')

    return results
