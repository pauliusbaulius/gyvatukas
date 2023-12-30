import pytest
from gyvatukas.utils.validators import validate_lt_id, LithuanianPersonalCodeSchema


@pytest.mark.parametrize(
    "pid, expected_result",
    [
        (
            "33309240064",
            LithuanianPersonalCodeSchema(
                gender="male",
                birth_year=1933,
                birth_month=9,
                birth_day=24,
                identifier_number="0064",
                is_edge_case=False,
                checksum=4,
            ),
        ),
        (
            "33300000064",
            LithuanianPersonalCodeSchema(
                gender="male",
                birth_year=1933,
                birth_month=None,
                birth_day=None,
                identifier_number="0064",
                is_edge_case=True,
                checksum=None,
            ),
        ),
    ],
)
def test_validate_lt_id(pid, expected_result) -> None:
    result = validate_lt_id(pid)
    assert result == expected_result
