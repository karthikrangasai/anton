from dataclasses import field
from pathlib import Path
from typing import List

from anton import yaml_conf

TEST_CASE = """integer_list:
  - 1
  - 2

string_list:
  - Hello
  - World

float_list:
  - 3.14
  - 6.9

bool_list:
  - true
  - false
"""


def test_simple_list_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_list.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleListConfiguration:
        float_list: List[float]
        bool_list: List[bool]
        integer_list: List[int] = field(default_factory=lambda: [34, 35])
        string_list: List[str] = field(default_factory=list)

    simple_list_obj = SimpleListConfiguration()
    assert sum(simple_list_obj.integer_list) == 3 and sum(simple_list_obj.integer_list) != 69
    assert " ".join(simple_list_obj.string_list) == "Hello World"
