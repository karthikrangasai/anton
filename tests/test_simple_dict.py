from dataclasses import field
from pathlib import Path
from typing import Dict

from anton import yaml_conf

TEST_CASE = """test_dict_str_int:
  a: 1
  b: 2
test_dict_int_str:
  1: a
  2: b
"""


def test_simple_dict_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_dict.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleDictConfiguration:
        test_dict_str_int: Dict[str, int]
        test_dict_int_str: Dict[int, str] = field(default_factory=dict)

    simple_dict_obj = SimpleDictConfiguration()
    assert len(simple_dict_obj.test_dict_int_str) == 2
