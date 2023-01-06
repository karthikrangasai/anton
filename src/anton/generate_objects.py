import dataclasses
import inspect
import typing
import warnings
from collections import OrderedDict
from typing import Any, Callable, Dict, Type, Union

from anton.constants import PRIMITIVE_TYPES


def generate_primitive_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_union_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_list_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_tuple_type_object(value: Any, parameter_type: Type) -> Any:
    return tuple(value)


def generate_dict_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_user_defined_class_object(value: Any, parameter_type: Type) -> Any:
    # NOTE: Assuming that the only classes can be dataclasses. `dataclasses.is_dataclass(value)` might be useful to check this later on.
    # `value` here will be a dictionary of the kwargs of the __init__ for the user-defined dataclass.
    if dataclasses.is_dataclass(parameter_type):
        raw_values: Dict[str, Any] = OrderedDict(value)
        value_fields: Dict[str, dataclasses.Field] = OrderedDict(getattr(parameter_type, "__dataclass_fields__"))

        kwargs = {
            arg_name: generate_object(value, field_properties.type)
            for ((arg_name, value), (arg_name, field_properties)) in zip(raw_values.items(), value_fields.items())
        }

        return parameter_type(**kwargs)

    raise NotImplementedError()


TYPE_TO_OBJECT_GENERATOR_MAPPING: Dict[Any, Callable[[Any, Type], Any]] = {
    dict: generate_dict_type_object,
    list: generate_list_type_object,
    tuple: generate_tuple_type_object,
    Union: generate_union_type_object,
}


def generate_object(value: Any, parameter_type: Type) -> Any:
    actual_type = typing.get_origin(parameter_type)

    if actual_type is not None:
        # Now dealing with container types
        # NOTE: Might need to check for being a subclass of `typing._GenericAlias`
        if actual_type not in TYPE_TO_OBJECT_GENERATOR_MAPPING:
            warnings.warn(
                f"Object generating code has not been written for {actual_type} yet. Will assume the type passes for now.",
                RuntimeWarning,
            )
            return True

        object_generator_function = TYPE_TO_OBJECT_GENERATOR_MAPPING[actual_type]
        return object_generator_function(value, parameter_type)

    # `parameter_type` is None: This could mean any primitve type, unsubscripted Union, user-defined class.
    if parameter_type not in PRIMITIVE_TYPES:
        if parameter_type is Union or parameter_type is Any:
            # NOTE: For the case when parameter_type is typing.Union (not subscripted)
            #       Assuming type `Any` -> Hence `True`
            return value

        # NOTE: Implement for case when parameter_type is a user-defined class
        if inspect.isclass(parameter_type):
            return generate_user_defined_class_object(value, parameter_type)

        # NOTE: Anything else that is missed will be raised as an error for now.
        raise NotImplementedError(
            f"Parsing and Type checking code has not been implemented for the type: {parameter_type} yet."
        )

    return generate_primitive_type_object(value, parameter_type)
