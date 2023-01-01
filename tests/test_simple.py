from pathlib import Path

from pyyamlconf import yaml_conf


def test_simple_yaml(simple_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_yaml_file_path)
    class SimpleConfiguration:
        string: str
        integer: int
        floating: float = 6.9
        boolean: bool = True

    simple_obj = SimpleConfiguration()
    assert simple_obj.floating != 6.9
    assert not simple_obj.boolean
