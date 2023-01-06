from typing import Any, Dict, List, Type, Union

import pytest

from anton.type_match import do_the_types_match, does_dict_type_match, does_list_type_match

LIST_MATCHING_EXAMPLES = [
    ([1, 2, 3], List[int], True),
    ([3.14, 9.8], List[float], True),
    (["Hello", "World"], List[str], True),
    ([True, False, True], List[bool], True),
    ([3.14, "is the value of PI"], List[float], False),
    ([3.14, "is the value of PI"], List[Union[str, float]], True),
    ([[3.14, "is the value of PI"], [9.8, "is the value of `g`"]], List[Union[str, float]], False),
    ([[3.14, "is the value of PI"], [9.8, "is the value of `g`"]], List[List[Union[str, float]]], True),
]

DICT_MATCHING_EXAMPLES = [
    ({1: 2, 2: 3, 3: 4}, Dict[int, int], True),
    ({"pi": 3.14, "g": 9.8}, Dict[str, float], True),
    ({"Hello": "World"}, Dict[str, str], True),
    ({"true": True, "false": False}, Dict[str, bool], True),
    ({3.14: "is the value of PI"}, Dict[str, float], False),
    ({3.14: "is the value of PI"}, Dict[float, int], False),
    ({3.14: "is the value of PI"}, Dict[int, str], False),
    ({3.14: "is the value of PI"}, Dict[float, Union[str, float]], True),
    (
        {"pi_value": [3.14, "is the value of PI"], "g_value": [9.8, "is the value of `g`"]},
        Dict[str, Union[str, float]],
        False,
    ),
    (
        {"pi_value": [3.14, "is the value of PI"], "g_value": [9.8, "is the value of `g`"]},
        Dict[str, List[Union[str, float]]],
        True,
    ),
]


@pytest.mark.parametrize(["value", "parameter_type", "does_match"], LIST_MATCHING_EXAMPLES)
def test_list_type_match_function(value: List[Any], parameter_type: Type, does_match: bool) -> None:
    assert does_list_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(["value", "parameter_type", "does_match"], DICT_MATCHING_EXAMPLES)
def test_dict_type_match_function(value: List[Any], parameter_type: Type, does_match: bool) -> None:
    assert does_dict_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(["value", "parameter_type", "does_match"], LIST_MATCHING_EXAMPLES + DICT_MATCHING_EXAMPLES)  # type: ignore
def test_type_match_function(value: List[Any], parameter_type: Type, does_match: bool) -> None:
    assert do_the_types_match(value=value, parameter_type=parameter_type) == does_match
