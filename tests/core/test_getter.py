import inspect
from dataclasses import MISSING, Field

import pytest

from anton.core.getter import get_init_arguments, get_value

ANTON_GETTER_IMPORT_PATH = "anton.core.getter"


def test_get_value() -> None:
    with pytest.raises(ValueError):
        get_value(dict(), "parameter", str, inspect._empty)

    with pytest.raises(TypeError):
        generated_value = get_value(
            dict(parameter=123), parameter_name="parameter", parameter_type=str, parameter_default="hello world"
        )

    generated_value = get_value(
        dict(parameter="value"), parameter_name="parameter", parameter_type=str, parameter_default="hello world"
    )
    assert generated_value == "value"


def test_get_init_arguments() -> None:
    conf_as_dict = {f"parameter{i}": f"value{i}" for i in range(5)}
    field_defaults = [MISSING, MISSING] + [f"value{i}" for i in range(2, 8)]
    dataclass_fields = {
        f"parameter{i}": Field(
            default=field_defaults[i],
            default_factory=MISSING,  # type: ignore
            init=i % 2 == 0,
            repr=i % 2 == 0,
            hash=None,
            compare=i % 2 == 0,
            metadata=None,  # type: ignore
        )
        for i in range(7)
    }
    actual_init_params = [
        ("parameter0", str, "hello"),
        ("parameter1", str, "world"),
        ("parameter2", str, "value2"),
        ("parameter3", str, "value3"),
    ]

    pos_args, kw_args = get_init_arguments(conf_as_dict, dataclass_fields, actual_init_params)

    assert pos_args == ("value0", "value1")
    assert kw_args == {"parameter2": "value2", "parameter3": "value3"}
