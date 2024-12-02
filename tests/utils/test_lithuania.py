import pytest
from gyvatukas.utils.lithuania import (
    validate_lt_id,
    LithuanianPersonalCode,
    validate_lt_tel_nr,
)


@pytest.mark.parametrize(
    "pid, expected_result",
    [
        (
            "33309240064",
            LithuanianPersonalCode(
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
            LithuanianPersonalCode(
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


@pytest.mark.parametrize(
    "tel, is_valid, formatted_tel",
    [
        ("+37061234567", True, "+37061234567"),
        ("861234567", True, "+37061234567"),
        ("061234567", True, "+37061234567"),  # New format from 2025.
        ("+37061234567aaa", True, "+37061234567"),  # Invalid characters are removed.
        ("+3.7.0.6.1.2.3.4.5.6.7!!!", True, "+37061234567"),
        ("cbb", False, "cbb"),  # Returns original string if invalid.
        ("+370612345678", False, "+370612345678"),
    ],
)
def test_validate_lt_tel_nr(tel, is_valid, formatted_tel) -> None:
    result = validate_lt_tel_nr(tel)
    assert result == (is_valid, formatted_tel)
