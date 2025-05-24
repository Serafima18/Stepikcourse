import pyparsing as pp

# h1
parse_h1 = pp.AtLineStart(pp.Keyword('#')) + pp.White() + (pp.restOfLine())('lesson_title')

# lesson_id
lesson_id_key = pp.Suppress('lesson_id' + pp.Optional(pp.White()) + ':')
lesson_id_value = pp.Word(pp.nums)('lesson_id')
parse_lesson_id = (lesson_id_key + lesson_id_value)

# lang
lang_key = pp.Suppress('lang' + pp.Optional(pp.White()) + ':')
lang_value = pp.Word(pp.alphanums + '_')('lang')
parse_lang = (lang_key + lang_value)

# h2
skip = pp.Literal("SKIP")("skip")
h2_start = pp.Literal("##")

task_types = ["TEXT", "QUIZ", "NUMBER", "STRING", "TASKINLINE", "MATCHING", "SPACE"]
task_type = pp.oneOf(task_types)("type")

header = pp.restOfLine("header")

parse_h2 = pp.AtLineStart(h2_start) + pp.Optional(skip) + pp.Optional(task_type, default="TEXT")\
             + pp.Optional(skip) + pp.Optional(pp.White()) + header


def parse_text(text):
    """
    Разбирает текс в формате markdown и возвращает словарь
    {
        'lesson_id': id урока,
        'lang': язык задач на программирование (опционально),
        'title': заголовок урока (только для человека, нигде не используется)
        'steps': [{
            'type': тип шага,
            'skip': пропускать шаг при апдейте или нет,
            'header': текст в теге <h2>,
            'text': текст шага в формате markdown одной строкой
       }]
    }
    """

    lines = [line for line in text.splitlines()]
    results = []
    
    current_h2 = None
    current_text = []
    lesson_data = {'steps': []}

    for line in lines:
        if parse_h1.matches(line):
            lesson_title_result = parse_h1.parseString(line)
            lesson_data['lesson_title'] = lesson_title_result.lesson_title

            continue

        elif len(results) < 0:
            continue

        if parse_lesson_id.matches(line):
            lesson_id_result = parse_lesson_id.parseString(line)
            lesson_data['lesson_id'] = lesson_id_result.lesson_id
            
            continue

        # elif len(results) < 1:
        #     continue

        if parse_lang.matches(line):
            lang_result = parse_lang.parseString(line)
            lesson_data['lang'] = lang_result.lang
            
            continue

        # elif len(results) < 2:
        #     continue

        if parse_h2.matches(line):
            if current_h2:
                current_h2['text'] = "\n".join(current_text)
                lesson_data['steps'].append(current_h2)
                # print('---------------------------------------------------------')
                # print(f'{current_text=}')
                # print('---------------------------------------------------------')
                current_text = []

            h2_current = parse_h2.parseString(line)
            current_h2 = {'type': h2_current.type,
                          'skip': 'True' if h2_current.skip else 'False', 
                          'header': h2_current.header,
                          'text': ''
                          }
            # print(f'{current_h2=}')
        elif current_h2:
            current_text.append(line)
            # print(f'{current_text=}')

    if current_h2:
        current_h2['text'] = "\n".join(current_text)
        lesson_data['steps'].append(current_h2)
        # print('---------------------------------------------------------')
        # print(f'{current_text=}')
        # print('---------------------------------------------------------')

    # print('===========================================================')
    print(lesson_data)

    return lesson_data
