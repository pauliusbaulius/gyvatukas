import logging

import requests

_logger = logging.getLogger("gyvatukas")


def get_my_ipv4(with_meta: bool = False) -> dict | str:
    """Lookup external ipv4 address. Uses https://ifconfig.me or https://wasab.is.

    🚨 Performs external request.
    """
    _logger.debug("performing ipv4 lookup.")
    url = "https://ifconfig.me" if with_meta else "https://wasab.is/json"

    result = requests.get(url=url, timeout=5)

    if with_meta:
        result = result.json()
    else:
        result = result.text

    _logger.debug("got ipv4 lookup json result `%s`.", result)

    return result


def get_ipv4_meta(ip: str) -> dict | None:
    """Lookup ipv4 information. Uses https://wasab.is.

    🚨 Performs external request.
    """
    _logger.debug("performing ipv4 meta lookup for ip `%s`.", ip)
    url = f"https://wasab.is/json?ip={ip}"

    result = requests.get(url=url, timeout=5)

    if result.status_code == 200:
        result = result.json()
    else:
        result = None

    _logger.debug("got ipv4 `%s` meta lookup json result `%s`.", ip, result)

    return result


def get_ip_country(ip: str) -> str:
    """Get country for given ip address or "Unknown" if not found."""
    data = get_ipv4_meta(ip)
    if data is None:
        return "Unknown"
    return data.get("country", "Unknown")
