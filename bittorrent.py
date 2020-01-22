from bencode import bdecode


class MetaInfoFile:

    def __init__(self, announce, info):
        self.announce = announce
        self.info = info


class Info:

    def __init__(self, name, piece_length, pieces, length, files, path):
        self.name = name
        self.piece_length = piece_length
        self.piece = pieces
        self.length = length
        self.files = files
        self.path = path

    def __str__(self) -> str:
        return super().__str__()


def decode(bencode_string):
    meta_info_decoded = bdecode(bencode_string)
    print(meta_info_decoded)
    announce = meta_info_decoded[b"announce"]
    info_decoded = meta_info_decoded[b"info"]

    info = Info(info_decoded[b"name"],
                info_decoded[b"piece length"],
                info_decoded[b"pieces"],
                info_decoded[b"length"],
                info_decoded.get(b"files"),
                info_decoded.get(b"path"))

    return MetaInfoFile(announce, info)


t = open("superman.torrent", "rb").readlines()
print(decode(b"".join(t)))

