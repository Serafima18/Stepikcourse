import pytest
from taskinline import config_section, test_section, other_section, task_parser, parse_task_text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from step_classes import Step


@pytest.mark.parametrize('text,expected', [
    ("CONFIG\nscore: 5\nvisible_tests: 2\nchecker: std_float_seq\nadditional_params: EPS: 0.001", {
        "score": "5",
        "visible_tests": "2",
        "checker": "std_float_seq",
        "additional_params": "EPS: 0.001"
    }),
    ("CONFIG\nscore: 15\nvisible_tests: all\nadditional_params: test_param", {
        "score": "15",
        "visible_tests": "all",
        "checker": "text",
        "additional_params": "test_param"
    })
])
def test_config_parsing(text, expected):
    assert config_section.matches(text)
    result = config_section.parseString(text)[0]
    assert result["type"] == "CONFIG"
    assert result["data"] == expected


@pytest.mark.parametrize('text,expected', [
    ("TEST\n1 2\n----\n3\n====\n4 5\n----\n9\n====", [
        {"input": "1 2", "output": "3"},
        {"input": "4 5", "output": "9"}
    ])
])
def test_test_section(text, expected):
    assert test_section.matches(text)
    result = test_section.parseString(text)[0]
    assert result["type"] == "TEST"
    assert result["data"] == expected


@pytest.mark.parametrize('text,expected_type,expected_data', [
    ("HEADER\n#include <stdio.h>", "HEADER", "#include <stdio.h>"),
    ("FOOTER\nreturn 0;", "FOOTER", "return 0;"),
    ("CODE\nint main() {}", "CODE", "int main() {}"),
])
def test_other_sections(text, expected_type, expected_data):
    assert other_section.matches(text)
    result = other_section.parseString(text)[0]
    assert result["type"] == expected_type
    assert result["data"] == expected_data


def test_full_task_parsing():
    text = """
Some condition text

CONFIG
score: 7
visible_tests: 1
checker: text
additional_params: param1

TEST
1 2\n----\n3\n====\n
CODE
int add(int a, int b) { return a + b; }

HEADER
#include <stdio.h>

FOOTER
return 0;
"""
    step = Step.parse(1, "Test title", text, "TASKINLINE")
    
    assert step.text.strip() == "<p>Some condition text</p>"
    assert step.config["score"] == 7
    assert step.config["visible_tests"] == 1
    assert step.config["checker"] == "text"
    assert step.config["additional_params"] == "param1"
    assert len(step.tests) == 1
    assert step.tests[0]["input"] == "1 2"
    assert step.tests[0]["output"] == "3"
    assert step.code == "\nint add(int a, int b) { return a + b; }"
    assert step.header == "\n#include <stdio.h>"
    assert step.footer == "\nreturn 0;"

test_full_task_parsing()