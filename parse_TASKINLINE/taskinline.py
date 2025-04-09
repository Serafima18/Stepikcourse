import pyparsing as pp


# Базовые элементы
section_keyword = pp.oneOf(["CODE", "HEADER", "FOOTER", "TEST", "CONFIG"])
colon = pp.Suppress(pp.Optional(pp.White()) + pp.Literal(":") + pp.Optional(pp.White()))
newline = pp.Suppress(pp.LineEnd())
stringEnd = pp.stringEnd

# Разделители тестов
test_delimiter = pp.Suppress(pp.Literal("----"))
test_end = pp.Suppress(pp.Literal("===="))


# CONFIG с поддержкой параметров
config_param = pp.oneOf(["score", "visible_tests", "checker", "additional_params"])
config_value = pp.restOfLine
config_line = config_param + colon + config_value

def parse_config(tokens):
    config = {
        "score": "10",
        "visible_tests": "all",
        "checker": "text",
        "additional_params": ""
    }
    
    for param, value in zip(tokens[1::2], tokens[2::2]):
        if param == "score":
            config["score"] = value

        elif param == "visible_tests":
            config["visible_tests"] = value

        elif param == "checker":
            if value.strip() not in ["text", "std_float_seq"]:
                return {}
            config["checker"] = value.strip()

        elif param == "additional_params":
            config["additional_params"] = value
    
    return config

config_section = (pp.Literal("CONFIG") + pp.OneOrMore(config_line)
    ).setParseAction(lambda t: {"type": "CONFIG", "data": parse_config(t)})


# TEST
test_input = pp.SkipTo(test_delimiter)
test_output = pp.SkipTo(test_end)

test_case = (test_input + test_delimiter + 
    test_output + test_end).setParseAction(
    lambda t: {"input": t[0].strip(), "output": t[1].strip()}
)

test_section = (pp.Literal("TEST") + 
    pp.OneOrMore(test_case)).setParseAction(
    lambda t: {"type": "TEST", "data": t[1:]})


# CODE, HEADER, FOOTER
content = pp.SkipTo(section_keyword | stringEnd)
other_section = (section_keyword + content).setParseAction(
    lambda t: {"type": t[0], "data": t[1].strip()})


# condition
task_condition = pp.SkipTo(section_keyword)

# all
task_parser = (
    task_condition("condition") + 
    pp.OneOrMore(
        pp.Group(test_section)("tests") | 
        pp.Group(config_section)("config") | 
        pp.Group(other_section)("other")
    )
)


def parse_task_text(text):
    if not task_parser.matches(text):
        print("Ошибка: текст не соответствует формату")
        return {}
    
    
    result = task_parser.parseString(text)

    parsed = {
        "condition": result["condition"],
        "CODE": "",
        "HEADER": "",
        "FOOTER": "",
        "TESTS": [],
        "CONFIG": {
            "score": 10,
            "visible_tests": "all",
            "checker": "text",
            "additional_params": ""
        }
    }
    
    for section in result[1:]:
        section = section[0]
        if section["type"] == "TEST":
            parsed["TESTS"].extend(section["data"])
        elif section["type"] == "CONFIG":
            config = section["data"]
            
            parsed["CONFIG"].update({
                "score": int(config.get("score", 10)),
                "visible_tests": (
                    int(config["visible_tests"]) 
                    if "visible_tests" in config and config["visible_tests"].isdigit()
                    else config.get("visible_tests", "all")
                ),
                "checker": config.get("checker", "text"),
                "additional_params": config.get("additional_params", "")
            })

        elif section["type"] in ["HEADER", "FOOTER", "CODE"]:
            parsed[section["type"]] = section["data"]
    
    if not parsed["TESTS"]:
        print("Ошибка: Обязательный блок TEST отсутствует")
        return {}
    
    return parsed
