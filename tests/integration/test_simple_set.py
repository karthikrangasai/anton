from dataclasses import field
from pathlib import Path
from typing import Any, Callable, Set, Union

import pytest

from anton import json_conf, yaml_conf

YAML_TEST_CASE = """single_type_set:
  - 1.0
  - 2.0
  - 2.0
  - 3.0
  - 4.0
union_type_set:
  - 1
  - abc
  - "1"
  - 2
  - abc
"""

JSON_TEST_CASE = """{
"single_type_set": [1.0,2.0,2.0,3.0,4.0],
"union_type_set": [1, "abc", "1", 2, "abc"]
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple_set.yaml", YAML_TEST_CASE, yaml_conf),
        ("base_dir_for_json_test_cases", "simple_set.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_set_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleSetConfiguration:
        single_type_set: Set[float]
        union_type_set: Set[Union[int, str]]

    simple_set_obj = test_func(SimpleSetConfiguration, conf_path=conf_path / file_name)()
    assert simple_set_obj.single_type_set == {1, 2, 3, 4}
    assert simple_set_obj.union_type_set == {1, 2, "1", "abc"}
