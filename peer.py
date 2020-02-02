import socket
from struct import pack

PSTR = b"BitTorrent protocol"
PEER_ID = b"-NL0001-NOOBLEARNING"


class Peer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self, info_hash=""):
        print("here")
        with socket.socket() as s:
            try:
                # s.bind(("127.0.0.1", 5000))
                print(self.ip, self.port)
                s.connect_ex((self.ip, self.port))
                print(s)
                print("Trying to handshake")
                handshake = Peer._handshake(info_hash)
                print(handshake)
                s.send(handshake)
                print("data")
                data = s.recv(68)
                print(data)
            except Exception as e:
                print(e)

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
        return pack(f">Bssss", len(PSTR), PSTR, b"00000000", info_hash, PEER_ID)
