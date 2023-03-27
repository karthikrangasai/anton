from pathlib import Path
from typing import Any, Callable

import pytest

from anton import json_conf, yaml_conf

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


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_any.yaml", YAML_TEST_CASE, yaml_conf),
        ("base_dir_for_json_test_cases", "simple_any.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_any(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleAnyConfiguration:
        any1: Any
        any2: Any
        any3: Any
        any4: Any = 1000

    simple_any_obj = test_func(SimpleAnyConfiguration, conf_path=conf_path / file_name)()
    assert simple_any_obj.any4 != 1000 and isinstance(simple_any_obj.any4, bool) and not simple_any_obj.any4
