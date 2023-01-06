from pathlib import Path
from typing import Optional

from anton import yaml_conf


def test_simple_optional_yaml(simple_optional_yaml_file_path: Path) -> None:
    @yaml_conf(conf_path=simple_optional_yaml_file_path)
    class SimpleOptionalConfiguration:
        non_optional: Optional[int] = None
        optional: Optional[int] = None
        true_optional: Optional[int] = None

    simple_optional_obj = SimpleOptionalConfiguration()
    assert simple_optional_obj.non_optional is not None
