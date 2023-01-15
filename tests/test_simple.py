from pathlib import Path

from anton import yaml_conf

TEST_CASE = """string: value
integer: 69
floating: 3.14
boolean: false
"""


def test_simple_yaml(base_dir_for_yaml_test_cases: Path) -> None:
    SIMPLE_YAML_TEST_CASE_PATH = base_dir_for_yaml_test_cases / "simple.yaml"

    with open(SIMPLE_YAML_TEST_CASE_PATH, "w") as fp:
        fp.write(TEST_CASE)

    @yaml_conf(conf_path=SIMPLE_YAML_TEST_CASE_PATH)
    class SimpleConfiguration:
        string: str
        integer: int
        floating: float = 6.9
        boolean: bool = True

    simple_obj = SimpleConfiguration()
    assert simple_obj.string == "value"
    assert simple_obj.integer == 69
    assert simple_obj.floating != 6.9 and simple_obj.floating == 3.14
    assert not simple_obj.boolean
