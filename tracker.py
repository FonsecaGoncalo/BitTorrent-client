import random
from enum import Enum, unique
from typing import List
from urllib.parse import urlencode
from urllib.request import urlopen


class Tracker:

    def __init__(self, info_hash: bytes, announce: List[List[str]]):
        self.info_hash = info_hash
        self.port = 6881
        self.peer_id = "-PY00000000000000000"
        self.announce = self._shuffle_announce(announce)
        self.event = None
        self.ip = None
        self.uploaded = 0
        self.downloaded = 0
        self.left = 0

    def order_trackers(self):
        for tier in self.announce:
            for tracker in tier:
                try:
                    tier.remove(tracker)
                    url = self._build_url(tracker)
                    print(url)
                    response = urlopen(url, timeout=5)
                    print(response.info())
                    print(response.read())
                    if response.getcode() == 200:
                        tier.insert(0, tracker)
                    else:
                        tier.append(tracker)
                except Exception:
                    tier.append(tracker)

    def _build_url(self, tracker):
        query_params = {
            "info_hash": self.info_hash,
            "peer_id": self.peer_id,
            "port": self.port,
            "uploaded": self.uploaded,
            "downloaded": self.downloaded,
            "left": self.left,
            "compact": 1,
        }

        return f"{tracker}?{urlencode(query_params)}"

    @staticmethod
    def _shuffle_announce(announce: List[List[str]]) -> List[List[str]]:
        # http://bittorrent.org/beps/bep_0012.html
        # Each tier is shuffle in order to help balance the load between the trackers
        for tier in announce:
            random.shuffle(tier)
        return announce

    @unique
    class _Event(Enum):
        STARTED = "started"
        COMPLETED = "completed"
        STOPPED = "stopped"
