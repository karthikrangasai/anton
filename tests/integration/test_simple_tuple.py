from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Tuple

import pytest

from anton import json_conf, toml_conf, yaml_conf

YAML_TEST_CASE = """single_value_tuple:
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

TOML_TEST_CASE = """single_value_tuple = [ 3.14,]
double_value_tuple = [ 1, "2",]
arbitrary_length_same_type_tuple = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,]
"""

JSON_TEST_CASE = """{
"single_value_tuple": [3.14],
"double_value_tuple": [1, "2"],
"arbitrary_length_same_type_tuple": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_tuple.yaml", YAML_TEST_CASE, yaml_conf),
        pytest.param(
            "base_dir_for_toml_test_cases",
            "simple_tuple.toml",
            TOML_TEST_CASE,
            toml_conf,
            marks=pytest.mark.xfail(reason="TOML can't decode non homogenous tuples. Example (1, '234')."),
        ),
        ("base_dir_for_json_test_cases", "simple_tuple.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_tuple_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleTupleConfiguration:
        single_value_tuple: Tuple[float]
        double_value_tuple: Tuple[int, str]
        arbitrary_length_same_type_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))

    simple_tuple_obj = test_func(SimpleTupleConfiguration, conf_path=conf_path / file_name)()
    assert sum(simple_tuple_obj.arbitrary_length_same_type_tuple) != 6
