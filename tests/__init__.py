from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
TESTS_EXAMPLE_ROOT = TESTS_ROOT / "example_yaml_files"

SIMPLE_USER_DEFINED_CLASS_YAML_TEST_FILE = TESTS_EXAMPLE_ROOT / "simple_user_defined_class.yaml"

__all__ = [
    "SIMPLE_USER_DEFINED_CLASS_YAML_TEST_FILE",
]
