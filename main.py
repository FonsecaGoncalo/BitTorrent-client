from torrent import Torrent

# read and parse the metainfo file (.torrent)
file = b"".join(open("torrentFiles/CentOS-7-x86_64-NetInstall-1708.torrent", "rb").readlines())
torrentt = Torrent.decode(file)

# Connect to tracker to get peers

torrentt.order_trackers()

# print(meta_info.info.piece)
