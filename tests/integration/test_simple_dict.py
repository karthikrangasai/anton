from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Dict

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_dict"

YAML_TEST_CASE = """test_dict_str_int:
  a: 1
  b: 2
test_dict_int_str:
  1: a
  2: b
"""

JSON_TEST_CASE = """{
"test_dict_str_int": {"a": 1,"b": 2},
"test_dict_int_str": {1: "a",2: "b"}
}"""


def test_simple_dict_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleDictConfiguration:
        test_dict_str_int: Dict[str, int]
        test_dict_int_str: Dict[int, str] = field(default_factory=dict)

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_dict_obj = SimpleDictConfiguration(conf_path=conf_path)
    assert len(simple_dict_obj.test_dict_int_str) == 2


@pytest.mark.xfail(reason="JSON cannot decode non string dictionary keys.")
def test_simple_dict_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleDictConfiguration:
        test_dict_str_int: Dict[str, int]
        test_dict_int_str: Dict[int, str] = field(default_factory=dict)

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_dict_obj = SimpleDictConfiguration(conf_path=conf_path)
    assert len(simple_dict_obj.test_dict_int_str) == 2
