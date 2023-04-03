from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, yaml_conf

FILENAME = "simple_any"

YAML_TEST_CASE = """any1: 1
any2: \"2\"
any3: 3.14
any4: False
"""

JSON_TEST_CASE = """{
"any1": 1,
"any2": \"2\",
"any3": 3.14,
"any4": false
}"""


def test_yaml_simple_any(base_dir_for_yaml_test_cases: Path) -> None:
    conf_path = base_dir_for_yaml_test_cases / f"{FILENAME}.yaml"

    @yaml_conf()
    class SimpleAnyConfiguration:
        any1: Any
        any2: Any
        any3: Any
        any4: Any = 1000

    with open(conf_path, "w") as fp:
        fp.write(YAML_TEST_CASE)

    simple_any_obj = SimpleAnyConfiguration(conf_path=conf_path)
    assert simple_any_obj.any4 != 1000 and isinstance(simple_any_obj.any4, bool) and not simple_any_obj.any4


def test_json_simple_any(base_dir_for_json_test_cases: Path) -> None:
    conf_path = base_dir_for_json_test_cases / f"{FILENAME}.json"

    @json_conf()
    class SimpleAnyConfiguration:
        any1: Any
        any2: Any
        any3: Any
        any4: Any = 1000

    with open(conf_path, "w") as fp:
        fp.write(JSON_TEST_CASE)

    simple_any_obj = SimpleAnyConfiguration(conf_path=conf_path)
    assert simple_any_obj.any4 != 1000 and isinstance(simple_any_obj.any4, bool) and not simple_any_obj.any4
