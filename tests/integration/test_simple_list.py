from dataclasses import field
from pathlib import Path
from typing import Any, Callable, List

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_list"

YAML_TEST_CASE = """integer_list:
  - 1
  - 2

string_list:
  - Hello
  - World

float_list:
  - 3.14
  - 6.9

bool_list:
  - true
  - false
"""

JSON_TEST_CASE = """{
"integer_list": [1, 2],
"string_list": ["Hello", "World"],
"float_list": [3.14, 6.9],
"bool_list": [true, false]
}"""


def test_simple_list_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleListConfiguration:
        float_list: List[float]
        bool_list: List[bool]
        integer_list: List[int] = field(default_factory=lambda: [34, 35])
        string_list: List[str] = field(default_factory=list)

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_list_obj = SimpleListConfiguration(conf_path=conf_path)
    assert sum(simple_list_obj.integer_list) == 3 and sum(simple_list_obj.integer_list) != 69
    assert " ".join(simple_list_obj.string_list) == "Hello World"


def test_simple_list_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleListConfiguration:
        float_list: List[float]
        bool_list: List[bool]
        integer_list: List[int] = field(default_factory=lambda: [34, 35])
        string_list: List[str] = field(default_factory=list)

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_list_obj = SimpleListConfiguration(conf_path=conf_path)
    assert sum(simple_list_obj.integer_list) == 3 and sum(simple_list_obj.integer_list) != 69
    assert " ".join(simple_list_obj.string_list) == "Hello World"
