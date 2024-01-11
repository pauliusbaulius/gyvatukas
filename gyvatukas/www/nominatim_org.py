import time
from threading import Lock

import requests

from gyvatukas.exceptions import GyvatukasException
from gyvatukas.www.base import BaseClient


class NominatimOrg(BaseClient):
    """Nominatim.org API client.

    🚨 Employs 1 request per second rate limit, as per Nominatim.org policy.
    See: https://operations.osmfoundation.org/policies/nominatim/
    """
    _LAST_CALL_TIME = 0
    _LOCK = Lock()
    RATE_LIMIT_PER_SECOND = 0.1

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        super().__init__(rate_limit_per_second=self.RATE_LIMIT_PER_SECOND)

    def rate_limit(self) -> None:
        with NominatimOrg._LOCK:
            time_elapsed = time.time() - NominatimOrg._LAST_CALL_TIME
            if time_elapsed < 1 / self.rate_limit_per_second:
                time.sleep((1 / self.rate_limit_per_second) - time_elapsed)
            NominatimOrg._LAST_CALL_TIME = time.time()

    def _get_request_headers(self) -> dict:
        """Return request headers."""
        return {
            "User-Agent": self.user_agent,
        }

    def resolve_coords_to_address(self, lat: float, lon: float) -> str:
        """Given lat/lon, return address."""
        self.rate_limit()
        raise NotImplementedError()

    def _parse_display_name(self, display_name: str) -> dict:
        """Parse `display_name` returned by nominatim.org, as it has the following structure:
        `amenity, street, city, county, state, postcode, country`
        """
        display_name = display_name.split(", ")
        data = {
            "amenity": display_name[0],
            "street": display_name[1],
            "city": display_name[2],
            "county": display_name[3],
            "state": display_name[4],
            "postcode": display_name[5],
            "country": display_name[6],
        }
        return data

    def resolve_address_to_coords(self, address: str) -> tuple[float, float]:
        """Given address, return coords as lat/lon.

        🚨 Precision required, since will return first match.
        """
        self.rate_limit()
        with requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": address,
                "format": "json",
                "limit": 1,
            },
            headers=self._get_request_headers(),
        ) as r:
            data = r.json()
            if not data:
                raise GyvatukasException(
                    f"Failed to resolve address `{address}` to coords!"
                )
            return float(data[0]["lat"]), float(data[0]["lon"])
