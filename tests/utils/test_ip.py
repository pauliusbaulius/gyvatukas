import pytest
from gyvatukas.utils.ip import get_ip_country


@pytest.mark.integration
@pytest.mark.parametrize(
    "ip, expected_result",
    [
        ("8.8.8.8", "United States"),
        ("0.0.0.0", "Unknown"),
    ],
)
def test_get_ip_country(ip, expected_result) -> None:
    result = get_ip_country(ip)
    assert result == expected_result
