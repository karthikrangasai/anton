from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from anton import json_conf, yaml_conf

YAML_TEST_CASE = """non_optional: 123
optional: null
"""

JSON_TEST_CASE = """{
"non_optional": 123,
"optional": null
}"""


@pytest.mark.parametrize(
    ("conf_path_fixture_name", "file_name", "test_case", "test_func"),
    [
        ("base_dir_for_yaml_test_cases", "simple.yaml", YAML_TEST_CASE, yaml_conf),
        ("base_dir_for_json_test_cases", "simple.json", JSON_TEST_CASE, json_conf),
    ],
)
def test_simple_optional_yaml(
    request: pytest.FixtureRequest,
    conf_path_fixture_name: str,
    file_name: str,
    test_case: str,
    test_func: Callable[..., Any],
) -> None:
    conf_path: Path = request.getfixturevalue(conf_path_fixture_name)

    with open(conf_path / file_name, "w") as fp:
        fp.write(test_case)

    class SimpleOptionalConfiguration:
        non_optional: Optional[int] = None
        optional: Optional[int] = None
        true_optional: Optional[int] = None

    simple_optional_obj = test_func(SimpleOptionalConfiguration, conf_path=conf_path / file_name)()
    assert simple_optional_obj.non_optional is not None
