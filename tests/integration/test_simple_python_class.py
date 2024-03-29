from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_python_class"

YAML_TEST_CASE = """first_point:
  args:
    - args:
        - abc
        - xyz
    - 10
second_point:
  kwargs:
    save_path:
      args:
        - abc
        - xyz
    x: 10
    y: 10
"""

JSON_TEST_CASE = """{
    "first_point":{"args": [{"args": ["abc", "xyz"]}, 10]},
    "second_point":{"kwargs": {"save_path": {"args": ["abc", "xyz"]}, "x": 10,"y": 10}}
}"""


class Point:
    def __init__(self, save_path: Path, x: int, y: int = 10) -> None:
        self.save_path = save_path
        self.x = x
        self.y = y

    def __eq__(self, __o: object) -> bool:
        return self.x == getattr(__o, "x") and self.y == getattr(__o, "y")


def test_simple_dict_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleDataclassConfiguration:
        first_point: Point
        second_point: Point = Point(Path(), 20, 20)

        def squared_distance(self) -> int:
            x_dist = self.second_point.x - self.first_point.x
            y_dict = self.second_point.y - self.first_point.y
            return pow(x_dist, 2) + pow(y_dict, 2)

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_user_defined_obj = SimpleDataclassConfiguration(conf_path=conf_path)
    print(simple_user_defined_obj)
    assert simple_user_defined_obj.first_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.second_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.squared_distance() == 0


def test_simple_dict_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleDataclassConfiguration:
        first_point: Point
        second_point: Point = Point(Path(), 20, 20)

        def squared_distance(self) -> int:
            x_dist = self.second_point.x - self.first_point.x
            y_dict = self.second_point.y - self.first_point.y
            return pow(x_dist, 2) + pow(y_dict, 2)

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_user_defined_obj = SimpleDataclassConfiguration(conf_path=conf_path)
    print(simple_user_defined_obj)
    assert simple_user_defined_obj.first_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.second_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.squared_distance() == 0
