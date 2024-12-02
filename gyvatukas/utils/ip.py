"""Relies on external services, no guarantees."""
import ipaddress
import logging

import httpx

from gyvatukas.utils.decorators import timer

_logger = logging.getLogger("gyvatukas")


@timer()
def get_my_ipv4() -> str:
    """Lookup external ipv4 address. Uses https://ifconfig.me or https://wasab.is.

    🚨 Performs external request.
    """
    _logger.debug("performing ipv4 lookup.")
    url = "https://wasab.is/json"

    result = httpx.get(url=url, timeout=5)
    data = result.json()
    return data["ip"]


@timer()
def get_ipv4_meta(ip: str) -> dict | None:
    """Lookup ipv4 information. Uses https://wasab.is.

    🚨 Performs external request.
    """
    _logger.debug("performing ipv4 meta lookup for ip `%s`.", ip)
    url = f"https://wasab.is/json?ip={ip}"

    result = httpx.get(url=url, timeout=5)

    if result.status_code == 200:
        result = result.json()
    else:
        result = None

    return result


@timer()
def get_ip_country(ip: str) -> str | None:
    """Get country for given ip address or "Unknown" if not found."""
    data = get_ipv4_meta(ip)
    if data is None:
        return None
    return data.get("country", "Unknown")


def ip_to_int(ip: str) -> int:
    return int(ipaddress.IPv4Address(ip))


def int_to_ip(ip_int: int) -> str:
    return str(ipaddress.IPv4Address(ip_int))


if __name__ == "__main__":
    my_ip = get_my_ipv4()
    print(my_ip)
    print(get_ip_country("8.8.8.8"))