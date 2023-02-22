import json
from pathlib import Path
from typing import Tuple, Type, Union

import pytest
import toml
import yaml

from anton.core.loader import json_load, toml_load, yaml_load

JSON_FILE_CONTENTS = """{"abc": 1,"xyz": 2}"""

YAML_FILE_CONTENTS = """abc: 1\nxyz: 2\n"""

TOML_FILE_CONTENTS = """abc = 1\nxyz = 2"""

PYTHON_OBJECT = {"abc": 1, "xyz": 2}


def common_test(
    anton_func,
    file_path: Path,
    correct_contents: str,
    wrong_contents: str,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]],
) -> None:

    with open(file_path, "w") as f:
        f.write(correct_contents)

    assert anton_func(file_path) == PYTHON_OBJECT

    with open(file_path, "w") as f:
        f.write(wrong_contents)

    with pytest.raises(exceptions):
        anton_func(file_path)


def test_json_load(base_dir_for_test_cases: Path) -> None:
    file_path = base_dir_for_test_cases / "test.json"
    common_test(json_load, file_path, JSON_FILE_CONTENTS, JSON_FILE_CONTENTS[1:], json.JSONDecodeError)


def test_yaml_load(base_dir_for_test_cases: Path) -> None:
    file_path = base_dir_for_test_cases / "test.yaml"
    common_test(yaml_load, file_path, YAML_FILE_CONTENTS, YAML_FILE_CONTENTS.replace(":", "=", 1), yaml.YAMLError)


def test_toml_load(base_dir_for_test_cases: Path) -> None:
    file_path = base_dir_for_test_cases / "test.toml"
    common_test(
        toml_load,
        file_path,
        TOML_FILE_CONTENTS,
        TOML_FILE_CONTENTS.replace("=", ":"),
        (TypeError, toml.TomlDecodeError, OSError, FileNotFoundError),
    )
