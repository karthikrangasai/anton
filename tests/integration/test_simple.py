from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple"

YAML_TEST_CASE = """string: value
integer: 69
floating: 3.14
boolean: false
"""

JSON_TEST_CASE = """{
"string": "value",
"integer": 69,
"floating": 3.14,
"boolean": false
}"""


def test_simple_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleConfiguration:
        string: str
        integer: int
        floating: float = 6.9
        boolean: bool = True

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_obj = SimpleConfiguration(conf_path=conf_path)
    assert simple_obj.string == "value"
    assert simple_obj.integer == 69
    assert simple_obj.floating != 6.9 and simple_obj.floating == 3.14
    assert not simple_obj.boolean


def test_simple_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleConfiguration:
        string: str
        integer: int
        floating: float = 6.9
        boolean: bool = True

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_obj = SimpleConfiguration(conf_path=conf_path)
    assert simple_obj.string == "value"
    assert simple_obj.integer == 69
    assert simple_obj.floating != 6.9 and simple_obj.floating == 3.14
    assert not simple_obj.boolean
