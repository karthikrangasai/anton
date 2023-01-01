import inspect
import typing
from dataclasses import MISSING as dataclass_missing_value
from dataclasses import Field, dataclass
from os import PathLike
from pathlib import Path
from typing import Any, Dict, Type, Union

import yaml

from pyyamlconf.constants import CONTAINER_TYPES, PRIMITIVE_TYPES

StrOrBytesPath = Union[str, Path, PathLike]


def do_the_types_match(value: Any, parameter_type: Type) -> bool:
    actual_type = typing.get_origin(parameter_type)

    if actual_type is None:
        if parameter_type in PRIMITIVE_TYPES:
            return isinstance(value, parameter_type)

        # NOTE: Implement for case when parameter_type is typing.Union (not subscripted)

    # Now dealing with container types
    # NOTE: Only solving for List type. List with single primitive (no Unions)
    # NOTE: Might need to check for being a subclass of `typing._GenericAlias`
    if actual_type is list:
        list_elements_type = typing.get_args(parameter_type)
        # NOTE: Assuming that the list elements are primitive types.

        is_actually_container_instance = isinstance(value, actual_type)  # type: ignore
        elements_obey_type = all([isinstance(element, list_elements_type) for element in value])
        return is_actually_container_instance and elements_obey_type

    return False


def _yaml_conf_wrapper(
    cls,
    /,
    *,
    conf_path: StrOrBytesPath,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
):

    dataclass_cls = dataclass(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)  # type: ignore
    actual_init = getattr(dataclass_cls, "__init__")
    setattr(dataclass_cls, "init_setter", actual_init)
    dataclass_fields: Dict[str, Field] = getattr(dataclass_cls, "__dataclass_fields__")

    # To ignore the self parameter, index from 1 to all.
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

            if not do_the_types_match(value=value, parameter_type=parameter_type):
                raise TypeError(f"{parameter_name} expects a value of type {parameter_type} but received {value}.")

            parameters_dataclass_field = dataclass_fields[parameter_name]

            if parameters_dataclass_field.default is dataclass_missing_value:
                pos_args.append(value)
                continue

            kw_args[parameter_name] = value

        getattr(self, "init_setter")(*pos_args, **kw_args)

    setattr(dataclass_cls, "__init__", modified_init)

    return dataclass_cls


def yaml_conf(
    cls=None,
    /,
    *,
    conf_path: StrOrBytesPath,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
):
    def wrap(cls):
        return _yaml_conf_wrapper(
            cls, conf_path=conf_path, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen
        )

    if cls is None:
        return wrap

    return wrap(cls)
