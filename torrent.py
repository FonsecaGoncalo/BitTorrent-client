from __future__ import annotations

from typing import List

from bencode import bdecode, bencode
from hashlib import sha1


class Info:

    def __init__(self, name, piece_length, pieces, length, files, path):
        self.name = name
        self.piece_length = piece_length
        self.piece = pieces
        self.length = length
        self.files = files
        self.path = path


class Torrent(object):

    def __init__(self, announce, info, info_hash):
        self.announce = announce
        self.info = info
        self.info_hash = info_hash

    @classmethod
    def decode(cls, bencoded_meta_info: bytes) -> Torrent:
        meta_info_decoded = bdecode(bencoded_meta_info)

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

        return cls(announce_decoded, info, info_hash)

    @staticmethod
    def _get_announce_decoded(meta_info_decoded: dict) -> List[List[str]]:
        """
         BEP 12 http://bittorrent.org/beps/bep_0012.html
         If the "announce-list" key is present, ignore the "announce" key and only use the URLs in "announce-list"
         """
        if b"announce-list" in meta_info_decoded:
            announce = meta_info_decoded[b"announce-list"]
        else:
            announce = meta_info_decoded[b"announce"]

        return [list(map(lambda tracker: tracker.decode("utf-8"), trackers)) for trackers in announce]

    @staticmethod
    def _split_pieces(pieces: bytes, piece_size: int) -> List[bytes]:
        return list(map(lambda index: pieces[index: index + piece_size], range(0, len(pieces), piece_size)))
