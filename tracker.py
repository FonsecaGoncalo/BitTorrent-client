import random
from enum import Enum, unique
from typing import List, Tuple, Iterable
from urllib.parse import urlencode
from urllib.request import urlopen
from struct import unpack
from bencoder import bdecode


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
                    self.request_peers(tracker)
                    tier.insert(0, tracker)
                except Exception:
                    tier.append(tracker)

    def request_peers(self, tracker) -> Iterable[Tuple[str, int]]:
        url = self._build_url(tracker)
        response_encoded = urlopen(url, timeout=5)

        if response_encoded.getcode() != 200:
            raise ConnectionError

        response = bdecode(response_encoded.read())
        peers = response[b'peers']
        # peers is be a string consisting of multiples of 6 byte
        peers_ips = list(map(lambda index: peers[index: index + 6], range(0, len(peers), 6)))

        def decode_peers(buffer) -> Tuple[str, int]:
            # First 4 bytes are the IP address and last 2 bytes are the port number.
            # All in network (big endian) notation

            # ! - network (= big-endian)
            # 4B - 4 * unsigned char -> integer
            # H - unsigned short ->  integer
            fmt = "!4BH"
            *ip_list, port = unpack(fmt, buffer)
            list_port = ".".join(map(str, ip_list)), port
            return list_port

        return list(map(decode_peers, peers_ips))

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
