from dataclasses import field
from pathlib import Path
from typing import Any, Callable, List

import pytest

from anton import json_conf, toml_conf, yaml_conf

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

TOML_TEST_CASE = """integer_list = [ 1, 2,]
string_list = [ "Hello", "World",]
float_list = [ 3.14, 6.9,]
bool_list = [ true, false,]
"""

JSON_TEST_CASE = """{
"integer_list": [1, 2],
"string_list": ["Hello", "World"],
"float_list": [3.14, 6.9],
"bool_list": [true, false]
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple.yaml", YAML_TEST_CASE, yaml_conf),
        ("base_dir_for_toml_test_cases", "simple.toml", TOML_TEST_CASE, toml_conf),
        ("base_dir_for_json_test_cases", "simple.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_list_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleListConfiguration:
        float_list: List[float]
        bool_list: List[bool]
        integer_list: List[int] = field(default_factory=lambda: [34, 35])
        string_list: List[str] = field(default_factory=list)

    simple_list_obj = test_func(SimpleListConfiguration, conf_path=conf_path / file_name)()
    assert sum(simple_list_obj.integer_list) == 3 and sum(simple_list_obj.integer_list) != 69
    assert " ".join(simple_list_obj.string_list) == "Hello World"
