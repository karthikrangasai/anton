from pathlib import Path

import pytest

import tests


@pytest.fixture(scope="session")
def simple_yaml_file_path() -> Path:
    return tests.SIMPLE_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_list_yaml_file_path() -> Path:
    return tests.SIMPLE_LIST_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_dict_yaml_file_path() -> Path:
    return tests.SIMPLE_DICT_YAML_TEST_FILE
