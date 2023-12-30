import pytest
from gyvatukas.utils.dict_ import dict_remove_matching_values


@pytest.mark.parametrize(
    "d, values, expected_result",
    [
        (
            {"a": 1, "b": None},
            [None],
            {"a": 1},
        ),
        (
            {"a": 1, "b": {"c": 1}},
            [{"c": 1}],
            {"a": 1},
        ),
        (
            {"a": 1, "b": {"c": 1}},
            [1],
            {"b": {"c": 1}},
        ),
        (
            # TODO: Does not work with nested data structures.
            {"a": 1, "b": {"b": {"a": 1}}},
            [{"a": 1}],
            {"a": 1, "b": {"b": {"a": 1}}},
        ),
    ],
)
def test_validate_lt_id(d, values, expected_result) -> None:
    result = dict_remove_matching_values(d=d, values=values)
    assert result == expected_result
