import inspect
from dataclasses import MISSING as dataclass_missing_value
from dataclasses import Field, dataclass
from os import PathLike
from pathlib import Path
from pprint import pprint
from typing import TYPE_CHECKING, Any, Dict, List, Union

import yaml

StrOrBytesPath = Union[str, Path, PathLike]


def _yaml_conf_wrapper(
    cls, /, *, conf_path: StrOrBytesPath, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False
):

    dataclass_cls = dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)  # type: ignore
    actual_init = getattr(dataclass_cls, "__init__")
    setattr(dataclass_cls, "init_setter", actual_init)
    dataclass_fields: Dict[str, Field] = getattr(dataclass_cls, "__dataclass_fields__")

    actual_init_params = [(x, y.annotation) for x, y in inspect.signature(actual_init).parameters.items()][1:]

    def modified_init(self) -> None:

        conf_as_dict: Dict[str, Any] = {}
        with open(conf_path) as stream:
            try:
                conf_as_dict.update(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                raise exc

        pos_args = []
        kw_args = {}

        for parameter_name, parameter_type in actual_init_params:
            if parameter_name not in conf_as_dict:
                raise ValueError(f"{parameter_name} is missing the definition of the YAML file at {conf_path}.")

            value = conf_as_dict.pop(parameter_name)

            if not isinstance(value, parameter_type):
                raise TypeError(f"{parameter_name} expects a value of type {parameter_type} but received {value}.")

            parameters_dataclass_field = dataclass_fields[parameter_name]

            if parameters_dataclass_field.default is dataclass_missing_value:
                pos_args.append(value)
                continue

            kw_args[parameter_name] = value

        getattr(self, "init_setter")(*pos_args, **kw_args)

    setattr(dataclass_cls, "__init__", modified_init)

    return dataclass_cls


def yaml_conf(cls=None, /, *, conf_path, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):
    def wrap(cls):
        return _yaml_conf_wrapper(
            cls, conf_path=conf_path, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen
        )

    if cls is None:
        return wrap

    return wrap(cls)
