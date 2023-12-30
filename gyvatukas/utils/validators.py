import datetime
import logging
from typing import Literal

import pydantic
from email_validator import validate_email, EmailNotValidError

_logger = logging.getLogger("gyvatukas")


def is_email_valid(email: str, check_deliverability: bool = False) -> tuple[bool, str]:
    """Check if email is valid. If check_deliverability is True, will also check if email is deliverable.
    If email is valid, returns normalized email, otherwise returns the original email.

    🚨 check_deliverability performs external request!

    Uses https://github.com/JoshData/python-email-validator lib.
    """
    _logger.debug("validating email `%s", email)
    try:
        validation_result = validate_email(
            email, check_deliverability=check_deliverability
        )
    except EmailNotValidError:
        _logger.exception(f"email `{email}` validation failed!")
        return False, email

    return True, validation_result.normalized


class LithuanianPersonalCodeSchema(pydantic.BaseModel):
    """Lithuanian personal identification code "asmens kodas" schema."""

    gender: Literal["male", "female"] | None
    birth_year: int
    birth_month: int | None
    birth_day: int | None
    identifier_number: str
    is_edge_case: bool
    checksum: int | None = None

    @property
    def birth_date(self) -> datetime.date | None:
        """Return birthdate as dt object if is not an edge case (has no 0 in month/day)."""
        if not self.is_edge_case:
            return datetime.date(self.birth_year, self.birth_month, self.birth_day)


def _calculate_lt_id_checksum(pid: str) -> int:
    """Calculate Lithuanian personal identification code "asmens kodas" checksum.
    See: https://lt.wikipedia.org/wiki/Asmens_kodas
    """
    weights_a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    weights_b = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]

    checksum_a = sum([int(pid[i]) * weights_a[i] for i in range(10)])
    checksum_a = checksum_a % 11

    if checksum_a != 10:
        return checksum_a

    checksum_b = sum([int(pid[i]) * weights_b[i] for i in range(10)])
    checksum_b = checksum_b % 11

    if checksum_b != 10:
        return checksum_b

    return 0


def validate_lt_id(pid: str) -> LithuanianPersonalCodeSchema:
    """Validate Lithuanian personal identification code "asmens kodas".
    See: https://lt.wikipedia.org/wiki/Asmens_kodas

    🚨 Does not check if it makes sense, e.g. birthdate is in the future or identifier number is valid.
    """
    is_edge_case = False

    if len(pid) != 11:
        raise Exception("PID should be 11 characters long!")

    gender_number = int(pid[0])
    birth_year = int(pid[1:3])
    birth_month = int(pid[3:5])
    birth_day = int(pid[5:7])

    # Wikipedia:
    # Asmens kodai, suteikiami vyresnio amžiaus žmonėms neprisimenantiems savo gimimo mėnesio ar dienos.
    # Tokiuose koduose vietoje mėnesio ar dienos skaitmenų įrašomi 0. Tai labai reta išimtis.
    if birth_month == 0:
        is_edge_case = True
        birth_month = None

    if birth_day == 0:
        is_edge_case = True
        birth_day = None

    identifier_number = pid[7:]

    # Validate first digit aka sex.
    if gender_number in [1, 3, 5]:
        gender = "male"
    elif gender_number in [2, 4, 6]:
        gender = "female"
    elif gender_number == 9:
        gender = None
        is_edge_case = True
    else:
        raise Exception(
            f"Invalid first number of PID `{gender_number}`, must be one of `1,2,3,4,5,6,9`!"
        )

    # Set base birth year.
    birth_base = 0
    if gender_number in [1, 2]:
        birth_base = 1800
    elif gender_number in [3, 4]:
        birth_base = 1900
    elif gender_number in [5, 6]:
        birth_base = 2000

    birth_year = birth_base + birth_year

    checksum = None
    if not is_edge_case:
        checksum = _calculate_lt_id_checksum(pid=pid)

    return LithuanianPersonalCodeSchema(
        gender=gender,
        birth_year=birth_year,
        birth_month=birth_month,
        birth_day=birth_day,
        identifier_number=identifier_number,
        is_edge_case=is_edge_case,
        checksum=checksum,
    )
