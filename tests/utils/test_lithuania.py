import datetime

import pytest
from gyvatukas.utils.lithuania import (
    validate_lt_tel_nr,
    LtIdValidationError,
    LithuanianPersonalCode,
    validate_lt_id,
    InvalidFormatError,
    InvalidGenderNumberError,
    InvalidBirthDateError,
    InvalidChecksumError,
    InvalidIdentifierError,
    FutureBirthDateError,
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
                identifier_number="006",  # Changed: identifier is 3 digits
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
                identifier_number="006",  # Changed: identifier is 3 digits
                is_edge_case=True,
                checksum=None,
            ),
        ),
    ],
)
def test_validate_lt_id_valid_cases(
    pid: str, expected_result: LithuanianPersonalCode
) -> None:
    result = validate_lt_id(pid)
    assert result == expected_result


@pytest.mark.parametrize(
    "pid, expected_exception",
    [
        ("1234", InvalidFormatError),  # Too short
        ("123456789012", InvalidFormatError),  # Too long
        ("1234567890A", InvalidFormatError),  # Non-digits
        ("73309240064", InvalidGenderNumberError),  # Invalid gender number
        ("33313240064", InvalidBirthDateError),  # Invalid month
        ("33309330064", InvalidBirthDateError),  # Invalid day
        ("33309241234", InvalidChecksumError),  # Wrong checksum (with valid identifier)
        ("33309240000", InvalidIdentifierError),  # Invalid identifier (000)
        ("53509240066", FutureBirthDateError),  # Future date (2035) with valid checksum
    ],
)
def test_validate_lt_id_invalid_cases(
    pid: str, expected_exception: type[LtIdValidationError]
) -> None:
    with pytest.raises(expected_exception):
        validate_lt_id(pid)


def test_birth_date_property() -> None:
    # Test normal case
    normal_case = LithuanianPersonalCode(
        gender="male",
        birth_year=1933,
        birth_month=9,
        birth_day=24,
        identifier_number="006",
        is_edge_case=False,
        checksum=4,
    )
    assert normal_case.birth_date == datetime.date(1933, 9, 24)

    # Test edge case
    edge_case = LithuanianPersonalCode(
        gender="male",
        birth_year=1933,
        birth_month=None,
        birth_day=None,
        identifier_number="006",
        is_edge_case=True,
        checksum=None,
    )
    assert edge_case.birth_date is None


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
