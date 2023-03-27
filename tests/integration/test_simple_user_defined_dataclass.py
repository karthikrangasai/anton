from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, yaml_conf

YAML_TEST_CASE = """first_point:
  x: 10
  y: 10
second_point:
  x: 10
  y: 10
"""

JSON_TEST_CASE = """{
"first_point":{"x": 10,"y": 10},
"second_point":{"x": 10,"y": 10}
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_user_defined_dataclasses.yaml", YAML_TEST_CASE, yaml_conf),
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

    @dataclass
    class Point:
        x: int
        y: int

    class SimpleDataclassConfiguration:
        first_point: Point
        second_point: Point = Point(20, 20)

        def squared_distance(self) -> int:
            x_dist = self.second_point.x - self.first_point.x
            y_dict = self.second_point.y - self.first_point.y
            return pow(x_dist, 2) + pow(y_dict, 2)

    simple_user_defined_obj = test_func(SimpleDataclassConfiguration, conf_path=conf_path / file_name)()
    assert simple_user_defined_obj.first_point == Point(10, 10)
    assert simple_user_defined_obj.second_point == Point(10, 10)
    assert simple_user_defined_obj.squared_distance() == 0
