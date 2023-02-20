from pathlib import Path
from typing import Any, Callable

import pytest

from anton import toml_conf, yaml_conf

YAML_TEST_CASE = """string: value
integer: 69
floating: 3.14
boolean: false
"""

TOML_TEST_CASE = """string = "value"
integer = 69
floating = 3.14
boolean = false
"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple.yaml", YAML_TEST_CASE, yaml_conf),
        ("base_dir_for_toml_test_cases", "simple.toml", TOML_TEST_CASE, toml_conf),
    ],
)
def test_simple_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleConfiguration:
        string: str
        integer: int
        floating: float = 6.9
        boolean: bool = True

    simple_obj = test_func(SimpleConfiguration, conf_path=conf_path / file_name)()
    assert simple_obj.string == "value"
    assert simple_obj.integer == 69
    assert simple_obj.floating != 6.9 and simple_obj.floating == 3.14
    assert not simple_obj.boolean
