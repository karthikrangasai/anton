import json
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Union

import yaml

StrOrBytesPath = Union[str, Path, PathLike]


def yaml_load(conf_path: StrOrBytesPath) -> Dict[str, Any]:
    conf_as_dict: Dict[str, Any] = {}
    with open(conf_path) as stream:
        try:
            conf_as_dict.update(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            raise exc
    return conf_as_dict


def json_load(conf_path: StrOrBytesPath) -> Dict[str, Any]:
    conf_as_dict: Dict[str, Any] = {}
    with open(conf_path) as stream:
        try:
            conf_as_dict.update(json.load(stream))
        except json.JSONDecodeError as error:
            raise error
    return conf_as_dict
