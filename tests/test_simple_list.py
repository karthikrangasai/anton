from dataclasses import field
from pathlib import Path
from typing import List

from pyyamlconf import yaml_conf


def test_simple_yaml(simple_list_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_list_yaml_file_path)
    class SimpleListConfiguration:
        float_list: List[float]
        bool_list: List[bool]
        integer_list: List[int] = field(default_factory=lambda: [34, 35])
        string_list: List[str] = field(default_factory=list)

    simple_obj = SimpleListConfiguration()
    assert sum(simple_obj.integer_list) == 3 and sum(simple_obj.integer_list) != 69
    assert " ".join(simple_obj.string_list) == "Hello World"
