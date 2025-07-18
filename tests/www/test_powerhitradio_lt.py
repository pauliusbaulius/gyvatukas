import pytest
from gyvatukas.www.powerhitradio_lt import PowerHitRadioLt


class TestPowerHitRadioLt:
    """Test PowerHitRadio client."""

    def test_init(self):
        """Test client initialization."""
        client = PowerHitRadioLt()
        assert client is not None

    @pytest.mark.integration
    def test_get_currently_playing(self):
        """Test getting currently playing song returns valid data."""
        client = PowerHitRadioLt()
        result = client.get_currently_playing()

        assert isinstance(result, dict)
        assert len(result) > 0
