from pathlib import Path
from typing import Any

from anton import yaml_conf

TEST_CASE = """any1: 1
any2: \"2\"
any3: 3.14
any4: False
"""


def test_simple_any_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_any.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleAnyConfiguration:
        any1: Any
        any2: Any
        any3: Any
        any4: Any = 1000

    simple_any_obj = SimpleAnyConfiguration()
    assert simple_any_obj.any4 != 1000 and isinstance(simple_any_obj.any4, bool) and not simple_any_obj.any4
