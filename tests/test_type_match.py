from typing import Any, List, Type, Union

import pytest

from pyyamlconf.type_match import do_the_types_match, does_list_type_match

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


@pytest.mark.parametrize(["value", "parameter_type", "does_match"], LIST_MATCHING_EXAMPLES)
def test_list_type_match_function(value: List[Any], parameter_type: Type, does_match: bool) -> None:
    assert does_list_type_match(value=value, parameter_type=parameter_type) == does_match


@pytest.mark.parametrize(["value", "parameter_type", "does_match"], LIST_MATCHING_EXAMPLES)
def test_type_match_function(value: List[Any], parameter_type: Type, does_match: bool) -> None:
    assert do_the_types_match(value=value, parameter_type=parameter_type) == does_match
