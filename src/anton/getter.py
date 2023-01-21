import inspect
from dataclasses import MISSING as DATACLASS_MISSING_VALUE
from dataclasses import Field
from typing import Any, Dict, List, Tuple

from anton.generate_objects import generate_object
from anton.type_match import do_the_types_match


def get_value(
    conf_as_dict: Dict[str, Any],
    parameter_name: str,
    parameter_type: Any,
    parameter_default: Any,
) -> Any:
    value = conf_as_dict.pop(parameter_name, parameter_default)
    if value == inspect._empty:
        raise ValueError(f"{parameter_name} missing in the configuration definition.")

    if not do_the_types_match(value=value, parameter_type=parameter_type):
        # FIXME: When tuple checking function fails, error message shows list type object in error message.
        #        Would be nice if we convert to tuple and show in the error.
        raise TypeError(f"{parameter_name} expects a value of type {parameter_type} but received {value}.")

    generated_value = generate_object(value=value, parameter_type=parameter_type)
    return generated_value


def get_init_arguments(
    conf_as_dict: Dict[str, Any],
    dataclass_fields: Dict[str, Field],
    actual_init_params: List[Tuple[str, Any, Any]],
) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
    pos_args = []
    kw_args = {}  # NOTE: Can possibly use typing._get_defaults.

    # To ignore the self parameter, index from 1 to all.
    for parameter_name, parameter_type, parameter_default in actual_init_params:
        generated_value = get_value(conf_as_dict, parameter_name, parameter_type, parameter_default)
        parameters_dataclass_field = dataclass_fields[parameter_name]

        if parameters_dataclass_field.default is DATACLASS_MISSING_VALUE:
            pos_args.append(generated_value)  # Encountered a positional argument. Append and continue.
            continue

        kw_args[parameter_name] = generated_value  # Fallback to keyword argument.

    return tuple(pos_args), kw_args
