import dataclasses
import inspect
import typing
import warnings
from collections import OrderedDict
from copy import deepcopy
from typing import Any, Callable, Dict, Generator, List, Type, Union

from anton.core.type_handlers.constants import PRIMITIVE_TYPES


def generate_primitive_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_union_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_list_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_set_type_object(value: Any, parameter_type: Type) -> Any:
    return set(value)


def generate_tuple_type_object(value: Any, parameter_type: Type) -> Any:
    return tuple(value)


def generate_dict_type_object(value: Any, parameter_type: Type) -> Any:
    return value


def generate_user_defined_class_object(value: Any, parameter_type: Type) -> Any:
    # NOTE: `value` here will be a dictionary of the kwargs of the __init__ for the user-defined dataclass.
    if dataclasses.is_dataclass(parameter_type):
        raw_values: Dict[str, Any] = OrderedDict(value)
        value_fields: Dict[str, dataclasses.Field] = OrderedDict(getattr(parameter_type, "__dataclass_fields__"))

        # Use only keyword arguments provided by the user.
        dataclass_kwargs = {
            arg_name: generate_object(value, value_fields[arg_name].type) for arg_name, value in raw_values.items()
        }
        return parameter_type(**dataclass_kwargs)

    # Generate Python object
    # All other non-dataclass Python classes.
    # Accept only two feilds:
    #       args   : list of positional arguments
    #       kwargs : dictionary of keyword arguments

    def get_type(_type: Type) -> Type:
        if _type == inspect._empty:
            return Any  # type: ignore
        return _type

    def next_provided_arg(cls_args_arguments: List[Any]) -> Generator[Union[Any, List[Any]], bool, None]:
        num_args = len(cls_args_arguments)
        i = 0
        while i < num_args:
            clear_all_args: bool = yield  # type: ignore
            if clear_all_args:
                yield cls_args_arguments[i:]

                i = num_args
            else:
                yield cls_args_arguments[i]
                i += 1

    if not isinstance(value, Dict):
        return False

    if not all(key in ["args", "kwargs"] for key in value.keys()):
        return False

    sig = inspect.signature(parameter_type)

    params = sig.parameters
    all_arguments_names = set(params.keys())
    visited_arguments = set()

    values = deepcopy(value)

    provided_args: List[Any] = values.get("args", [])
    provided_kwargs: Dict[str, Any] = values.get("kwargs", {})

    visited_kinds = set()

    pos_args = []
    kw_args = {}

    gen = next_provided_arg(provided_args)
    for _, (name, parameter) in enumerate(params.items()):
        if name in visited_arguments:
            raise ValueError("Argument was already passed.")

        visited_arguments.add(name)
        all_arguments_names.discard(name)
        visited_kinds.add(parameter.kind)

        is_keyword_argument = (
            parameter.kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD and parameter.name in provided_kwargs
        ) or (parameter.kind == inspect._ParameterKind.KEYWORD_ONLY)

        is_positional_argument = (
            parameter.kind == inspect._ParameterKind.POSITIONAL_OR_KEYWORD and parameter.name not in provided_kwargs
        ) or (parameter.kind == inspect._ParameterKind.POSITIONAL_ONLY)

        if is_positional_argument:
            try:
                next(gen)
                val = gen.send(False)  # type: ignore
                obj = generate_object(val, get_type(parameter.annotation))
                pos_args.append(obj)
            except StopIteration as e:
                # Exhausted all the args
                pass

        elif is_keyword_argument:
            if name not in provided_kwargs:
                pass
            val = provided_kwargs.pop(parameter.name)
            obj = generate_object(val, get_type(parameter.annotation))
            kw_args[name] = obj
        elif parameter.kind == inspect._ParameterKind.VAR_POSITIONAL:
            try:
                next(gen)  # have to call -  to get to the next yield statement
                val = gen.send(True)  # type: ignore
            except StopIteration as e:
                val = []

            obj = [generate_object(_val, get_type(parameter.annotation)) for _val in val]
            pos_args.extend(obj)
        elif parameter.kind == inspect._ParameterKind.VAR_KEYWORD:
            obj = {name: generate_object(_val, get_type(parameter.annotation)) for key, _val in provided_kwargs.items()}
            kw_args.update(obj)

    return parameter_type(*pos_args, **kw_args)


TYPE_TO_OBJECT_GENERATOR_MAPPING: Dict[Any, Callable[[Any, Type], Any]] = {
    dict: generate_dict_type_object,
    list: generate_list_type_object,
    tuple: generate_tuple_type_object,
    Union: generate_union_type_object,
    set: generate_set_type_object,
}


def generate_object(value: Any, parameter_type: Type) -> Any:
    actual_type = typing.get_origin(parameter_type)

    if actual_type is not None:
        # Now dealing with container types
        if actual_type not in TYPE_TO_OBJECT_GENERATOR_MAPPING:
            warnings.warn(
                f"Object generating code has not been written for {actual_type} yet. Will assume the type passes for now.",
                RuntimeWarning,
            )
            return True

        object_generator_function = TYPE_TO_OBJECT_GENERATOR_MAPPING[actual_type]
        return object_generator_function(value, parameter_type)

    # `parameter_type` is None: This could mean any primitve type, unsubscripted Union, user-defined class.
    if parameter_type in PRIMITIVE_TYPES:
        return generate_primitive_type_object(value, parameter_type)

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
