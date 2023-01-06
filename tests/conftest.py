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


@pytest.fixture(scope="session")
def simple_tuple_yaml_file_path() -> Path:
    return tests.SIMPLE_TUPLE_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_user_defined_class_yaml_file_path() -> Path:
    return tests.SIMPLE_USER_DEFINED_CLASS_YAML_TEST_FILE
