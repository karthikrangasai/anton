from pathlib import Path
from pprint import pprint
from dataclasses import dataclass
from anton import yaml_conf
from typing import Any, List, Dict, Optional, Tuple
import pytest
import enum
from jsonargparse import CLI

DEV_DIR = Path(__file__).resolve().parent.absolute()
INDEX_YAML = DEV_DIR / "index.yaml"


# class XYZ:
#     def __init__(self, x: int, y: int = 10) -> None:
#         self.x = x
#         self.y = y

#     def __call__(self) -> Any:
#         return self.x + self.y


# class Point:
#     def __init__(self, save_path: Path, x: int, y: int = 10) -> None:
#         self.save_path = save_path
#         self.x = x
#         self.y = y

#     def __eq__(self, __o: "Point") -> bool:
#         return self.x == __o.x and self.y == __o.y

#     def __repr__(self) -> str:
#         return f"Point(x={self.x}, y={self.y}, save_path={self.save_path})"


# @yaml_conf(conf_path=DEV_DIR / "test.yaml")
# class TestClass:
#     first_point: Point
#     second_point: Point = Point(Path("xyz", "abc"), 20, 20)

#     def squared_distance(self) -> int:
#         x_dist = self.second_point.x - self.first_point.x
#         y_dict = self.second_point.y - self.first_point.y
#         return pow(x_dist, 2) + pow(y_dict, 2)


# print(TestClass())


@yaml_conf()
class Class:
    x: int
    y: float


c = Class(conf_path="./dev/y.yaml")
print(c)
