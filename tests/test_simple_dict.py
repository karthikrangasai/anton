from dataclasses import field
from pathlib import Path
from typing import Dict

from pyyamlconf import yaml_conf


def test_simple_dict_yaml(simple_dict_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_dict_yaml_file_path)
    class SimpleDictConfiguration:
        test_dict_str_int: Dict[str, int]
        test_dict_int_str: Dict[int, str] = field(default_factory=dict)

    simple_dict_obj = SimpleDictConfiguration()
    assert len(simple_dict_obj.test_dict_int_str) == 2
