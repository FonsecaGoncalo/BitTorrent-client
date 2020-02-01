from __future__ import annotations

import asyncio
from hashlib import sha1
from typing import List

from bencoder import bencode, bdecode

from tracker import Tracker


class Info:

    def __init__(self, name, piece_length, pieces, length, files, path):
        self.name = name
        self.piece_length = piece_length
        self.piece = pieces
        self.length = length
        self.files = files
        self.path = path
        self.queue = asyncio.Queue(50)


class Torrent(object):

    def __init__(self, announce, info, info_hash, tracker):
        self.server = None
        self.announce = announce
        self.info = info
        self.info_hash = info_hash
        self.tracker = tracker

    def order_trackers(self):
        self.tracker.order_trackers()

    @classmethod
    def decode(cls, encoded_meta_info: bytes) -> Torrent:
        meta_info_decoded = bdecode(encoded_meta_info)
        info_decoded = meta_info_decoded[b"info"]
        info_hash = sha1(bencode(info_decoded)).digest()

        announce_decoded = cls._get_announce_decoded(meta_info_decoded)

        # pieces maps to a string whose length is a multiple of 20. It is to be subdivided into strings of length 20,
        # each of which is the SHA1 hash of the piece at the corresponding index
        pieces = cls._split_pieces(info_decoded[b"pieces"], sha1().digest_size)

        info = Info(info_decoded[b"name"].decode("utf-8"),
                    info_decoded[b"piece length"],
                    pieces,
                    info_decoded.get(b"length"),
                    info_decoded.get(b"files"),
                    info_decoded.get(b"path"))

        tracker = cls._build_tracker(info_hash, announce_decoded)

        return cls(announce_decoded, info, info_hash, tracker)

    @staticmethod
    def _build_tracker(info_hash: bytes, announces: List[List[str]]) -> Tracker:
        return Tracker(info_hash, announces)

    @staticmethod
    def _get_announce_decoded(meta_info_decoded: dict) -> List[List[str]]:
        # BEP 12 http://bittorrent.org/beps/bep_0012.html
        # If the "announce-list" key is present, ignore the "announce" key and only use the URLs in "announce-list"
        if b"announce-list" in meta_info_decoded:
            announce = meta_info_decoded[b"announce-list"]
            return [list(map(lambda tracker: tracker.decode("utf-8"), trackers)) for trackers in announce]
        else:
            return [[meta_info_decoded[b"announce"].decode("utf-8")]]

    @staticmethod
    def _split_pieces(pieces: bytes, piece_size: int) -> List[bytes]:
        return list(map(lambda index: pieces[index: index + piece_size], range(0, len(pieces), piece_size)))
