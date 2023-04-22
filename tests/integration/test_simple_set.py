from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Set, Union

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_set"

YAML_TEST_CASE = """single_type_set:
  - 1.0
  - 2.0
  - 2.0
  - 3.0
  - 4.0
union_type_set:
  - 1
  - abc
  - "1"
  - 2
  - abc
"""

JSON_TEST_CASE = """{
"single_type_set": [1.0,2.0,2.0,3.0,4.0],
"union_type_set": [1, "abc", "1", 2, "abc"]
}"""


def test_simple_set_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleSetConfiguration:
        single_type_set: Set[float]
        union_type_set: Set[Union[int, str]]

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_set_obj = SimpleSetConfiguration(conf_path=conf_path)
    assert simple_set_obj.single_type_set == {1, 2, 3, 4}
    assert simple_set_obj.union_type_set == {1, 2, "1", "abc"}


def test_simple_set_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleSetConfiguration:
        single_type_set: Set[float]
        union_type_set: Set[Union[int, str]]

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_set_obj = SimpleSetConfiguration(conf_path=conf_path)
    assert simple_set_obj.single_type_set == {1, 2, 3, 4}
    assert simple_set_obj.union_type_set == {1, 2, "1", "abc"}
