import requests

from gyvatukas.exceptions import GyvatukasException


class NominatimOrg:
    """Nominatim.org API client.

    🚨 Do not abuse this API, max 1 req/s as stated in the usage policy.
    See: https://operations.osmfoundation.org/policies/nominatim/
    """

    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    def _get_request_headers(self) -> dict:
        """Return request headers."""
        return {
            "User-Agent": self.user_agent,
        }

    def resolve_coords_to_address(self, lat: float, lon: float) -> str:
        """Given lat/lon, return address."""
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
