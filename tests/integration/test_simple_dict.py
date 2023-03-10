from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Dict

import pytest

from anton import json_conf, toml_conf, yaml_conf

YAML_TEST_CASE = """test_dict_str_int:
  a: 1
  b: 2
test_dict_int_str:
  1: a
  2: b
"""

TOML_TEST_CASE = """[test_dict_str_int]
a = 1
b = 2

[test_dict_int_str]
1 = "a"
2 = "b"
"""

JSON_TEST_CASE = """{
"test_dict_str_int": {"a": 1,"b": 2},
"test_dict_int_str": {1: "a",2: "b"}
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_dict.yaml", YAML_TEST_CASE, yaml_conf),
        pytest.param(
            "base_dir_for_toml_test_cases",
            "simple_dict.toml",
            TOML_TEST_CASE,
            toml_conf,
            marks=pytest.mark.xfail(reason="TOML can't decode non string dictionary keys."),
        ),
        pytest.param(
            "base_dir_for_json_test_cases",
            "simple_dict.json",
            JSON_TEST_CASE,
            json_conf,
            marks=pytest.mark.xfail(reason="JSON can't decode non string dictionary keys."),
        ),
    ],
)
def test_simple_dict_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleDictConfiguration:
        test_dict_str_int: Dict[str, int]
        test_dict_int_str: Dict[int, str] = field(default_factory=dict)

    simple_dict_obj = test_func(SimpleDictConfiguration, conf_path=conf_path / file_name)()
    assert len(simple_dict_obj.test_dict_int_str) == 2
