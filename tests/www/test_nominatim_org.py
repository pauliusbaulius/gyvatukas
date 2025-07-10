import pytest
from gyvatukas.www.nominatim_org import NominatimOrg


class TestNominatimOrg:
    """Test Nominatim client."""

    def test_init(self):
        """Test client initialization."""
        client = NominatimOrg("test-user-agent")
        assert client is not None
        assert client.user_agent == "test-user-agent"

    def test_get_request_headers(self):
        """Test request headers generation."""
        client = NominatimOrg("test-user-agent")
        headers = client._get_request_headers()
        
        assert "User-Agent" in headers
        assert headers["User-Agent"] == "test-user-agent"

    @pytest.mark.integration
    def test_resolve_coords_to_address(self):
        """Test resolving coordinates to address returns valid string."""
        client = NominatimOrg("gyvatukas-test")
        # Test with Vilnius coordinates
        result = client.resolve_coords_to_address(lat=54.6872, lon=25.2797)
        
        # Check that we got a string response
        assert isinstance(result, str)
        # Check that the response has some content
        assert len(result) > 0
        # Should contain some location information
        assert "Vilnius" in result or "Lithuania" in result

    @pytest.mark.integration
    def test_resolve_address_to_coords(self):
        """Test resolving address to coordinates returns valid tuple."""
        client = NominatimOrg("gyvatukas-test")
        # Test with Vilnius address
        result = client.resolve_address_to_coords("Vilnius, Lithuania")
        
        # Check that we got a tuple response
        assert isinstance(result, tuple)
        assert len(result) == 2
        # Check that coordinates are valid (latitude between -90 and 90, longitude between -180 and 180)
        lat, lon = result
        # Convert to float since Nominatim returns coordinates as strings
        lat_float = float(lat)
        lon_float = float(lon)
        assert -90 <= lat_float <= 90
        assert -180 <= lon_float <= 180
