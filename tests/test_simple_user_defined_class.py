from dataclasses import dataclass
from pathlib import Path

from anton import yaml_conf

TEST_CASE = """first_point:
  x: 10
  y: 10
second_point:
  x: 10
  y: 10
"""


def test_simple_dict_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_user_defined_dataclasses.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @dataclass
    class Point:
        x: int
        y: int

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleDataclassConfiguration:
        first_point: Point
        second_point: Point = Point(20, 20)

        def squared_distance(self) -> int:
            x_dist = self.second_point.x - self.first_point.x
            y_dict = self.second_point.y - self.first_point.y
            return pow(x_dist, 2) + pow(y_dict, 2)

    simple_user_defined_obj = SimpleDataclassConfiguration()
    assert simple_user_defined_obj.first_point == Point(10, 10)
    assert simple_user_defined_obj.second_point == Point(10, 10)
    assert simple_user_defined_obj.squared_distance() == 0
