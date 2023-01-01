from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
TESTS_EXAMPLE_ROOT = TESTS_ROOT / "example_yaml_files"

SIMPLE_YAML_TEST_FILE = TESTS_EXAMPLE_ROOT / "simple.yaml"
SIMPLE_LIST_YAML_TEST_FILE = TESTS_EXAMPLE_ROOT / "simple_list.yaml"

__all__ = [
    "SIMPLE_YAML_TEST_FILE",
    "SIMPLE_LIST_YAML_TEST_FILE",
]
