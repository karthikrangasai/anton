from dataclasses import field
from pathlib import Path
from typing import Tuple

from anton import yaml_conf


def test_simple_tuple_yaml(simple_tuple_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_tuple_yaml_file_path)
    class SimpleTupleConfiguration:
        single_value_tuple: Tuple[float]
        double_value_tuple: Tuple[int, str]
        arbitrary_length_same_type_tuple: Tuple[int, ...]

    simple_tuple_obj = SimpleTupleConfiguration()
    assert sum(simple_tuple_obj.arbitrary_length_same_type_tuple) == 55
