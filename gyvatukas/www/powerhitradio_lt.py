import requests

from gyvatukas.utils.dt import get_dt_utc_now

# TODO: Rate limit 1 req/s.


class PowerHitRadioLt:
    URL_CURRENTLY_PLAYING = "https://powerhitradio.tv3.lt/stream/player4/getsong"

    def get_currently_playing(self) -> dict:
        """Get currently playing song from Power Hit Radio LT.

        Returns parsed result, original response is stored in `_raw` key.
        """
        with requests.post(
            url=self.URL_CURRENTLY_PLAYING, data={"action": "getsong"}
        ) as response:
            data = response.json()
            if data.get("song") == "song":
                return {
                    "is_song": True,
                    "artist": data["artistName"],
                    "title": data["songTitle"],
                    "time": get_dt_utc_now(),
                    "_raw": data,
                }
            else:
                return {
                    "is_song": False,
                    "title": data["songTitle"],
                    "time": get_dt_utc_now(),
                    "_raw": data,
                }
