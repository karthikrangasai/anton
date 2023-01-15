from dataclasses import field
from pathlib import Path
from typing import Tuple

from anton import yaml_conf

TEST_CASE = """single_value_tuple:
  - 3.14
double_value_tuple:
  - 1
  - "2"
arbitrary_length_same_type_tuple:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
  - 9
  - 10
"""


def test_simple_tuple_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_tuple.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleTupleConfiguration:
        single_value_tuple: Tuple[float]
        double_value_tuple: Tuple[int, str]
        arbitrary_length_same_type_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))

    simple_tuple_obj = SimpleTupleConfiguration()
    assert sum(simple_tuple_obj.arbitrary_length_same_type_tuple) != 6
