from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_optional"

YAML_TEST_CASE = """non_optional: 123
optional: null
"""

JSON_TEST_CASE = """{
"non_optional": 123,
"optional": null
}"""


def test_simple_optional_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleOptionalConfiguration:
        non_optional: Optional[int] = None
        optional: Optional[int] = None
        true_optional: Optional[int] = None

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_optional_obj = SimpleOptionalConfiguration(conf_path=conf_path)
    assert simple_optional_obj.non_optional is not None


def test_simple_optional_json(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleOptionalConfiguration:
        non_optional: Optional[int] = None
        optional: Optional[int] = None
        true_optional: Optional[int] = None

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_optional_obj = SimpleOptionalConfiguration(conf_path=conf_path)
    assert simple_optional_obj.non_optional is not None
