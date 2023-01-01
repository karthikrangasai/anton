import typing
import warnings
from typing import Any, Callable, Dict, List, Type, Union

from pyyamlconf.constants import CONTAINER_TYPES, PRIMITIVE_TYPES


def does_primitive_type_match(value: Any, parameter_type: Type) -> bool:
    return isinstance(value, parameter_type)


def does_union_type_match(value: Any, parameter_type: Type) -> bool:
    union_types = typing.get_args(parameter_type)
    return isinstance(value, union_types)


def does_list_type_match(value: Any, parameter_type: Type) -> bool:
    # NOTE: Assuming only List[primitive_type], List[Union[primitive_types, ...]]
    # TODO: Consider cases like List[Tuple[...]], List[Dict[..., ...]], multiple nested stuff.

    # List will have only one type. Hence indexing the first element.
    list_elements_type = typing.get_args(parameter_type)[0]
    container_obeys_type = isinstance(value, List)
    elements_obey_type = all([do_the_types_match(element, list_elements_type) for element in value])
    return container_obeys_type and elements_obey_type


def does_dict_type_match(value: Any, parameter_type: Type) -> bool:
    # NOTE: Assuming only
    #       1. Dict[primitive_type, primitive_type]
    #       2. Dict[primitive_type, Union[primitive_type, ...]]
    #       2. Dict[Union[primitive_type, ...], primitive_type]
    #       2. Dict[Union[primitive_type, ...], Union[primitive_type, ...]]
    # TODO: Consider cases like Dict[..., Dict[..., ...]], Dict[Tuple[...], Dict[..., ...]], multiple nested stuff.
    key_elements_type, value_elements_type = typing.get_args(parameter_type)
    container_obeys_type = isinstance(value, Dict)
    keys_obey_type = all([do_the_types_match(element, key_elements_type) for element in value.keys()])
    values_obey_type = all([do_the_types_match(element, value_elements_type) for element in value.values()])
    return container_obeys_type and keys_obey_type and values_obey_type


def does_user_defined_class_match(value: Any, parameter_type: Type) -> bool:
    # TODO: Check whether the yaml dict exactly matches the `__init__` params of the user-defined class.
    #       Then we can do `user_defined_class(**yaml_provided_dict)`.
    raise NotImplementedError()


TYPE_TO_MATCHER_MAPPING: Dict[Any, Callable[[Any, Type], bool]] = {
    dict: does_dict_type_match,
    list: does_list_type_match,
    Union: does_union_type_match,
}


def do_the_types_match(value: Any, parameter_type: Type) -> bool:
    actual_type = typing.get_origin(parameter_type)

    if actual_type is not None:
        # Now dealing with container types
        # NOTE: Might need to check for being a subclass of `typing._GenericAlias`
        if actual_type not in TYPE_TO_MATCHER_MAPPING:
            warnings.warn(
                f"Type matching code has been written for {actual_type} yet. Will assume the type passes for now.",  # type: ignore
                RuntimeWarning,
            )
            return True

        type_checker_function = TYPE_TO_MATCHER_MAPPING[actual_type]
        return type_checker_function(value, parameter_type)

    # `parameter_type` is None: This could mean any primitve type, unsubscripted Union, user-defined class.
    if parameter_type not in PRIMITIVE_TYPES:
        if actual_type is Union:
            # NOTE: For the case when parameter_type is typing.Union (not subscripted)
            #       Assuming type `Any` -> Hence `True`
            return True

        # NOTE: Implement for case when parameter_type is a user-defined class
        raise NotImplementedError()

    return does_primitive_type_match(value, parameter_type)
