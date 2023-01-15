from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def base_dir_for_test_cases(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("test_cases_dir")


@pytest.fixture(scope="session")
def base_dir_for_yaml_test_cases(base_dir_for_test_cases: Path) -> Path:
    YAML_TEST_CASES_DIR = base_dir_for_test_cases / "yaml"
    YAML_TEST_CASES_DIR.mkdir(parents=True, exist_ok=True)
    return YAML_TEST_CASES_DIR
