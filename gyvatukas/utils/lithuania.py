import re
from typing import Literal
import datetime

import pydantic

from gyvatukas.utils.string import remove_except


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


def get_lt_nearby_pashtomatas_by_address(address: str) -> list[str]:
    """Get nearby 'paštomatai' by an address.

    🚨 Address should be in Lithuania.
    """
    raise NotImplementedError


def get_lt_nearby_pashtomatas_by_lat_lon(lat: float, lon: float) -> list[str]:
    """Get nearby 'paštomatai' by lat/lon values.

    🚨 Lat/lon should be in Lithuania.
    """
    raise NotImplementedError


def validate_lt_tel_nr(tel_nr: str, format_370: bool = True) -> tuple[bool, str]:
    """Validate Lithuanian phone number. Return if is valid and formatted number.

    Lithuanian number may start with +370, 8 or 0, followed by 8 digits.

    🚨 Does not check if it exists lol.
    ❗ Does not validate short numbers like 112, 1848, etc.
    """
    is_valid = False

    # Remove all symbols except + and 0-9.
    clean_tel_nr = remove_except(tel_nr, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+"])

    # Check if valid.
    regex = r"^(?:\+370|8|0)\d{8}$"
    if re.match(regex, clean_tel_nr):
        is_valid = True

    # If starts with 0 or 8, make it +370.
    if format_370 and clean_tel_nr.startswith("8") or clean_tel_nr.startswith("0"):
        clean_tel_nr = f"+370{tel_nr[1:]}"

    return is_valid, clean_tel_nr if is_valid else tel_nr
