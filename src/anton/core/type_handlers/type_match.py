import dataclasses
import inspect
import typing
import warnings
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from anton.core.type_handlers.constants import PRIMITIVE_TYPES

NONE_TYPE = type(None)


def does_primitive_type_match(value: Any, parameter_type: Type) -> bool:
    return isinstance(value, parameter_type)


def does_union_type_match(value: Any, parameter_type: Type) -> bool:
    union_types = typing.get_args(parameter_type)

    # Optional[T] -> Union[T, None]
    if len(union_types) == 2 and union_types[1] is NONE_TYPE:
        is_value_of_desired_type = do_the_types_match(value, union_types[0])
        is_value_none = value is None
        return is_value_of_desired_type or is_value_none

    return any(do_the_types_match(value, union_parameter_type) for union_parameter_type in union_types)


def does_any_type_match(value: Any, parameter_type: Type) -> bool:
    return True


def does_list_type_match(value: Any, parameter_type: Type) -> bool:
    # List will have only one type. Hence indexing the first element.
    list_elements_type = typing.get_args(parameter_type)[0]
    container_obeys_type = isinstance(value, List)
    if not container_obeys_type:
        return False
    elements_obey_type = all([do_the_types_match(element, list_elements_type) for element in value])
    return elements_obey_type


def does_tuple_type_match(value: Any, parameter_type: Type) -> bool:
    # We recieve the value as `List` althought the type will be `Tuple`. Making sure it is a List.
    container_obeys_type = isinstance(value, (List, Tuple))  # type: ignore
    if not container_obeys_type:
        return False
    # Tuple can have two ways of typing.
    #   - Tuple[T_1, T_2, ....., T_n] : For `i` assert do_the_types_match(value[i], T_i)
    #   - Tuple[T, ...] : For `i` assert do_the_types_match(value[i], T)

    tuple_elements_type = typing.get_args(parameter_type)
    if len(tuple_elements_type) == 2 and tuple_elements_type[1] == Ellipsis:
        # Tuple[T, ...] Case
        elements_obey_type = all([do_the_types_match(element, tuple_elements_type[0]) for element in value])
        return container_obeys_type and elements_obey_type

    # Tuple[T_1, T_2, ....., T_n] Default Case
    if len(tuple_elements_type) != len(value):
        return False

    elements_obey_type = all([do_the_types_match(element, _type) for element, _type in zip(value, tuple_elements_type)])
    return elements_obey_type


def does_dict_type_match(value: Any, parameter_type: Type) -> bool:
    key_elements_type, value_elements_type = typing.get_args(parameter_type)
    container_obeys_type = isinstance(value, Dict)
    if not container_obeys_type:
        return False

    keys_obey_type = all([do_the_types_match(element, key_elements_type) for element in value.keys()])
    values_obey_type = all([do_the_types_match(element, value_elements_type) for element in value.values()])
    return keys_obey_type and values_obey_type


def does_user_defined_class_match(value: Any, parameter_type: Type) -> bool:
    # TODO: Check whether the yaml dict exactly matches the `__init__` params of the user-defined class.
    #       Then we can do `user_defined_class(**yaml_provided_dict)`.

    # NOTE: Assuming that the only classes can be dataclasses. `dataclasses.is_dataclass(value)` might be useful to check this later on.
    # `value` here will be a dictionary of the kwargs of the __init__ for the user-defined dataclass.
    if dataclasses.is_dataclass(parameter_type):
        raw_values: Dict[str, Any] = OrderedDict(value)
        value_fields: Dict[str, dataclasses.Field] = OrderedDict(getattr(parameter_type, "__dataclass_fields__"))

        return all(
            do_the_types_match(value, field_properties.type)
            for ((arg_name, value), (arg_name, field_properties)) in zip(raw_values.items(), value_fields.items())
        )

    # NOTE: Anything else that is missed will be raised as an error for now.
    raise NotImplementedError(
        f"Parsing and Type checking code has not been implemented for the type: {parameter_type} yet."
    )


TYPE_TO_MATCHER_MAPPING: Dict[Any, Callable[[Any, Type], bool]] = {
    dict: does_dict_type_match,
    list: does_list_type_match,
    tuple: does_tuple_type_match,
    Any: does_any_type_match,
    Union: does_union_type_match,
}


def do_the_types_match(value: Any, parameter_type: Type) -> bool:
    actual_type = typing.get_origin(parameter_type)

    if actual_type is not None:
        # Now dealing with container types
        if actual_type not in TYPE_TO_MATCHER_MAPPING:
            warnings.warn(
                f"Type matching code has not been written for {actual_type} yet. Will assume the type passes for now.",
                RuntimeWarning,
            )
            return True

        type_checker_function = TYPE_TO_MATCHER_MAPPING[actual_type]
        return type_checker_function(value, parameter_type)

    # `parameter_type` is None: This could mean any primitve type, unsubscripted Union, user-defined class.
    if parameter_type in PRIMITIVE_TYPES:
        return does_primitive_type_match(value, parameter_type)

    if parameter_type is Union or parameter_type is Any:
        # NOTE: For the case when parameter_type is typing.Union (not subscripted)
        #       Assuming type `Any` -> Hence `True`
        return does_any_type_match(value, parameter_type)

    # NOTE: Implement for case when parameter_type is a user-defined class
    if inspect.isclass(parameter_type):
        return does_user_defined_class_match(value, parameter_type)

    # NOTE: Anything else that is missed will be raised as an error for now.
    raise NotImplementedError(
        f"Parsing and Type checking code has not been implemented for the type: {parameter_type} yet."
    )
