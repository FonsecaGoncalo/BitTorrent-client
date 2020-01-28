import torrent
from torrent import Torrent

# read and parse the metainfo file (.torrent)
file = b"".join(open("torrentFiles/CentOS-7-x86_64-NetInstall-1708.torrent", "rb").readlines())
meta_info = Torrent.decode(file)

# Connect to tracker to get peers

print(meta_info.info_hash)

# print(meta_info.info.piece)
