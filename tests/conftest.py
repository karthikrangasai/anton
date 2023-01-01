from pathlib import Path

import pytest

from tests import TESTS_EXAMPLE_ROOT


@pytest.fixture(scope="session")
def simple_yaml_file_path() -> Path:
    return TESTS_EXAMPLE_ROOT / "simple.yaml"
