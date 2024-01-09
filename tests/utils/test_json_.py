import os
import pytest
from gyvatukas.utils.json_ import load_json


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (
            "{}",
            {},
        ),
        (
            "[]",
            [],
        ),
        (
            '{"foo": "bar"}',
            {"foo": "bar"},
        ),
        (
            '[{"foo": "bar"}]',
            [{"foo": "bar"}],
        ),
        (
            '{"foo": "bar",}',
            {"foo": "bar"},
        ),
        (
            '[[{"foo": "bar"}]]',
            [[{"foo": "bar"}]],
        ),
        # Cases with ' instead of ".
        (
                "[{'foo': 'bar'}]",
                [{"foo": "bar"}],
        ),
        (
                "[{'foo': 'ba'r'}]",
                [{"foo": "ba'r"}],
        ),
    ],
)
def test_load_json(data, expected_result) -> None:
    result = load_json(data=data)
    assert result == expected_result
