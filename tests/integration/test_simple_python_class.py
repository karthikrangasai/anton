from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, toml_conf, yaml_conf

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

TOML_TEST_CASE = """[first_point]
args = [ 10,]

[second_point.kwargs]
x = 10
y = 10
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


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_user_defined_dataclasses.yaml", YAML_TEST_CASE, yaml_conf),
        pytest.param(
            "base_dir_for_toml_test_cases",
            "simple_user_defined_dataclasses.toml",
            TOML_TEST_CASE,
            toml_conf,
            marks=pytest.mark.xfail(reason="TOML can't nest Dict inside List inside Dict etc."),
        ),
        ("base_dir_for_json_test_cases", "simple_user_defined_dataclasses.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_dict_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleDataclassConfiguration:
        first_point: Point
        second_point: Point = Point(Path(), 20, 20)

        def squared_distance(self) -> int:
            x_dist = self.second_point.x - self.first_point.x
            y_dict = self.second_point.y - self.first_point.y
            return pow(x_dist, 2) + pow(y_dict, 2)

    simple_user_defined_obj = test_func(SimpleDataclassConfiguration, conf_path=conf_path / file_name)()
    print(simple_user_defined_obj)
    assert simple_user_defined_obj.first_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.second_point == Point(Path("abc", "xyz"), 10, 10)
    assert simple_user_defined_obj.squared_distance() == 0
