from pathlib import Path

import pytest

import tests


@pytest.fixture(scope="session")
def base_dir_for_test_cases(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("test_cases_dir")


@pytest.fixture(scope="session")
def base_dir_for_yaml_test_cases(base_dir_for_test_cases: Path) -> Path:
    YAML_TEST_CASES_DIR = base_dir_for_test_cases / "yaml"
    YAML_TEST_CASES_DIR.mkdir(parents=True, exist_ok=True)
    return YAML_TEST_CASES_DIR


@pytest.fixture(scope="session")
def simple_dict_yaml_file_path() -> Path:
    return tests.SIMPLE_DICT_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_tuple_yaml_file_path() -> Path:
    return tests.SIMPLE_TUPLE_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_optional_yaml_file_path() -> Path:
    return tests.SIMPLE_OPTIONAL_YAML_TEST_FILE


@pytest.fixture(scope="session")
def simple_user_defined_class_yaml_file_path() -> Path:
    return tests.SIMPLE_USER_DEFINED_CLASS_YAML_TEST_FILE
