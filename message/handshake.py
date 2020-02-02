from struct import pack
from message.message import Message

PSTR = b"BitTorrent protocol"
PEER_ID = b"-NL0001-NOOBLEARNING"
RESERVED = b"\x00" * 8

LENGTH_V1 = len(PSTR) + 49


class Handshake(Message):

    def get_id(self):
        return -1

    def handle(self):
        pass

    @staticmethod
    def from_info_hash(info_hash) -> bytes:
        # handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        #
        # pstrlen: string length of <pstr>, as a single raw byte
        #
        # pstr: string identifier of the protocol
        #
        # reserved: eight (8) reserved bytes. All current implementations use all zeroes.
        #   Each bit in these bytes can be used to change the behavior of the protocol.
        #
        # info_hash: 20-byte SHA1 hash of the info key in the metainfo file.
        #   This is the same info_hash that is transmitted in tracker requests.
        #
        # peer_id: 20-byte string used as a unique ID for the client.
        return pack(f">B{len(PSTR)}s8s20s20s", len(PSTR), PSTR, RESERVED, info_hash, PEER_ID)
