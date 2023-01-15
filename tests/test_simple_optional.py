from pathlib import Path
from typing import Optional

from anton import yaml_conf

TEST_CASE = """non_optional: 123
optional: null
"""


def test_simple_optional_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple_optional.yaml"

    with open(TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=TEST_CASE_PATH)
    class SimpleOptionalConfiguration:
        non_optional: Optional[int] = None
        optional: Optional[int] = None
        true_optional: Optional[int] = None

    simple_optional_obj = SimpleOptionalConfiguration()
    assert simple_optional_obj.non_optional is not None
