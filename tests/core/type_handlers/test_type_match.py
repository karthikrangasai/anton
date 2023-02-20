from typing import Any, Dict, List, Tuple, Type, Union

import pytest

import anton.core.type_handlers.type_match as tm

ARG_NAMES = ["does_match", "value", "parameter_type"]

PRIMITIVE_MATCHING_EXAMPLES = [
    (True, 1, int),
    (True, 1.0, float),
    (True, "1", str),
    (True, True, bool),
    (False, 1, bool),
    (False, 1, float),
    (False, 1, str),
]

LIST_MATCHING_EXAMPLES = [
    (True, [1, 2, 3], List[int]),
    (True, [3.14, 9.8], List[float]),
    (True, ["Hello", "World"], List[str]),
    (True, [True, False, True], List[bool]),
    (True, [3.14, "is the value of PI"], List[Union[str, float]]),
    (True, [[3.14, "is the value of PI"], [9.8, "is the value of `g`"]], List[List[Union[str, float]]]),
    (False, [3.14, "is the value of PI"], List[float]),
    (False, [[3.14, "is the value of PI"], [9.8, "is the value of `g`"]], List[Union[str, float]]),
]

DICT_MATCHING_EXAMPLES = [
    (True, {1: 2, 2: 3, 3: 4}, Dict[int, int]),
    (True, {"pi": 3.14, "g": 9.8}, Dict[str, float]),
    (True, {"Hello": "World"}, Dict[str, str]),
    (True, {"true": True, "false": False}, Dict[str, bool]),
    (True, {3.14: "is the value of PI"}, Dict[float, Union[str, float]]),
    (True, {"pi_value": [3.14, "constant PI"], "g_value": [9.8, "constant g"]}, Dict[str, List[Union[str, float]]]),
    (False, {3.14: "is the value of PI"}, Dict[str, float]),
    (False, {3.14: "is the value of PI"}, Dict[float, int]),
    (False, {3.14: "is the value of PI"}, Dict[int, str]),
    (False, {"pi_value": [3.14, "constant PI"], "g_value": [9.8, "constant g"]}, Dict[str, Union[str, float]]),
]

TUPLE_MATCHING_EXAMPLES = [
    (True, (1,), Tuple[int]),
    (True, (1, 1.0, "1", True), Tuple[int, float, str, bool]),
    (True, ([1, 2, 3], {1: 2, 3: 4}), Tuple[List[int], Dict[int, int]]),
    (True, (1, 2, 3, 4, 5), Tuple[int, ...]),
    (True, ([1, 2, 3], {1: 2, "3": False}, ["1", 2, 3.0]), Tuple[Union[Dict[Any, Any], List[Any]], ...]),
    (False, (1, 2, 3, 4, 5), Tuple[int, int, int, int]),
    (False, ([1, 2, 3], {1: 2, "3": False}, ["1", 2, 3.0]), Tuple[Union[Dict[Any, Any], List[Any]]]),
    (False, ([1, 2, 3], {1: 2, "3": False}), Tuple[Dict[Any, Any], List[Any]]),
]

ALL_EXAMPLES = PRIMITIVE_MATCHING_EXAMPLES + LIST_MATCHING_EXAMPLES + DICT_MATCHING_EXAMPLES + TUPLE_MATCHING_EXAMPLES  # type: ignore


@pytest.mark.parametrize(ARG_NAMES, PRIMITIVE_MATCHING_EXAMPLES)
def test_primitive_type_match_function(does_match: bool, value: List[Any], parameter_type: Type) -> None:
    assert tm.does_primitive_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(ARG_NAMES, LIST_MATCHING_EXAMPLES)
def test_list_type_match_function(does_match: bool, value: List[Any], parameter_type: Type) -> None:
    assert tm.does_list_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(ARG_NAMES, DICT_MATCHING_EXAMPLES)
def test_dict_type_match_function(does_match: bool, value: List[Any], parameter_type: Type) -> None:
    assert tm.does_dict_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(ARG_NAMES, TUPLE_MATCHING_EXAMPLES)
def test_tuple_type_match_function(does_match: bool, value: List[Any], parameter_type: Type) -> None:
    assert tm.does_tuple_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(ARG_NAMES, ALL_EXAMPLES)
def test_type_match_function(does_match: bool, value: List[Any], parameter_type: Type) -> None:
    assert tm.do_the_types_match(value=value, parameter_type=parameter_type) == does_match
