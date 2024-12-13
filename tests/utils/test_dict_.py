import pytest
from gyvatukas.utils.dict_ import dict_remove_matching_values, dict_get_by_path


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


@pytest.mark.parametrize(
    "data, path, expected_result",
    [
        ({"a": 1}, "a", 1),
        ({"a": {"b": 2}}, "a.b", 2),
        ({"a": [1, 2, 3]}, "a.0", 1),
        ({"a": [1, 2, 3]}, "a.2", 3),
        ({"a": (1, 2, 3)}, "a.1", 2),
        ({"users": [{"name": "John"}, {"name": "Jane"}]}, "users.1.name", "Jane"),
        ({"data": {"items": [{"id": 1}, {"id": 2}]}}, "data.items.0.id", 1),
        ({"a": 1}, "", {"a": 1}),
        (
            {"a": [1, 2, {"b": [3, 4]}]},
            "a.2.b.0",
            3,
        ),
    ],
)
def test_get_by_path_success(data, path, expected_result, separator="."):
    assert dict_get_by_path(data, path, separator) == expected_result
