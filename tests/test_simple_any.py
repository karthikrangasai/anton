from pathlib import Path
from typing import Any

from anton import yaml_conf


def test_simple_any_yaml(simple_any_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_any_yaml_file_path)
    class SimpleAnyConfiguration:
        any1: Any
        any2: Any
        any3: Any
        any4: Any = 1000

    simple_any_obj = SimpleAnyConfiguration()
    assert simple_any_obj.any4 != 1000
