from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Tuple

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_tuple"

YAML_TEST_CASE = """single_value_tuple:
  - 3.14
double_value_tuple:
  - 1
  - "2"
arbitrary_length_same_type_tuple:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
  - 9
  - 10
"""

JSON_TEST_CASE = """{
"single_value_tuple": [3.14],
"double_value_tuple": [1, "2"],
"arbitrary_length_same_type_tuple": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
}"""


def test_simple_tuple_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleTupleConfiguration:
        single_value_tuple: Tuple[float]
        double_value_tuple: Tuple[int, str]
        arbitrary_length_same_type_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_tuple_obj = SimpleTupleConfiguration(conf_path=conf_path)
    assert sum(simple_tuple_obj.arbitrary_length_same_type_tuple) != 6


def test_simple_tuple_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleTupleConfiguration:
        single_value_tuple: Tuple[float]
        double_value_tuple: Tuple[int, str]
        arbitrary_length_same_type_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_tuple_obj = SimpleTupleConfiguration(conf_path=conf_path)
    assert sum(simple_tuple_obj.arbitrary_length_same_type_tuple) != 6
