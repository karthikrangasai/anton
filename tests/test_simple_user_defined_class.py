from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from anton import yaml_conf


def test_simple_dict_yaml(simple_user_defined_class_yaml_file_path: Path) -> None:
    @dataclass
    class Point:
        x: int
        y: int

    @yaml_conf(conf_path=simple_user_defined_class_yaml_file_path)
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
