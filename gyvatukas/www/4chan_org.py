import pathlib

import requests

from gyvatukas.exceptions import GyvatukasException


class FourChanOrg:
    def rip_thread(self, thread_id: str, output_dir: pathlib.Path) -> None:
        """Given a thread_id, rips all media from the thread to the output_dir together with thread metadata.
        If output dir already contains data, will not re-download it.
        """
        raise NotImplementedError()

        url = f"https://a.4cdn.org/c/thread/{thread_id}.json"
        with requests.get(url=url, timeout=15) as response:
            if response.status_code != 200:
                raise GyvatukasException("Failed to get thread data!")
