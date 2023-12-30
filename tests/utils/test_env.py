import os
import pytest
from gyvatukas.utils.env import get_env


@pytest.mark.parametrize(
    "name, type, default, required, variable, expected_result",
    [
        ("FOO", str, None, False, "bar", "bar"),
    ],
)
def test_get_env(name, type, default, required, variable, expected_result) -> None:
    os.environ[name] = variable
    result = get_env(name=name, type=type, default=default, required=required)
    assert result == expected_result
