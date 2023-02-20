from pathlib import Path

import pytest
import toml
import yaml

from anton.core.loader import toml_load, yaml_load

YAML_FILE_CONTENTS = """xyz: 123\n456: "abc"\n"""
YAML_OBJECT = {"xyz": 123, 456: "abc"}

TOML_FILE_CONTENTS = """abc = 1\nxyz = 2"""
TOML_OBJECT = {"abc": 1, "xyz": 2}


def test_yaml_load(base_dir_for_test_cases: Path) -> None:

    file_path = base_dir_for_test_cases / "test.yaml"

    with open(file_path, "w") as f:
        f.write(YAML_FILE_CONTENTS)

    assert yaml_load(file_path) == YAML_OBJECT

    with open(file_path, "w") as f:
        f.write(YAML_FILE_CONTENTS.replace(":", "", 1))

    with pytest.raises(yaml.YAMLError):
        yaml_load(file_path)


def test_toml_load(base_dir_for_test_cases: Path) -> None:
    file_path = base_dir_for_test_cases / "test.toml"

    with open(file_path, "w") as f:
        f.write(TOML_FILE_CONTENTS)

    assert toml_load(file_path) == TOML_OBJECT

    with open(file_path, "w") as f:
        f.write(TOML_FILE_CONTENTS.replace(" = ", "", 1))

    with pytest.raises((TypeError, toml.TomlDecodeError, OSError, FileNotFoundError)):
        toml_load(file_path)
