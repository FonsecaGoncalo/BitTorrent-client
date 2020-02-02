import socket
from struct import pack

PSTR = b"BitTorrent protocol"
PEER_ID = b"-NL0001-NOOBLEARNING"
RESERVED = b"\x00" * 8


class Peer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

#    def connect(self, info_hash=""):
#        print("here")
#        with socket.socket() as s:
#            try:
#                print(self.ip, self.port)
#                s.connect((self.ip, self.port))
#                print(s)
#                print("Trying to handshake")
#                handshake = Peer._handshake(info_hash)
#                print(handshake)
#                s.send(handshake)
#                bitfieald = self._bitfield()
#                print(bitfieald)
#                s.send(bitfieald)
#                while True:
#                    data = s.recv(68)
#                    if len(data) > 0:
#                        print("data")
#                        print(data)
#            except Exception as e:
#                print(e)

    @staticmethod
    def _handshake(info_hash):
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

    @staticmethod
    def _bitfield():
        # bitfield: <len=0001+X><id=5><bitfield>
        array = bytearray(b"\x00" * 1304)
        return pack(f">IB{len(array)}s", 1305, 5, array)
