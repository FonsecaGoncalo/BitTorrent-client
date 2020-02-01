from torrent import Torrent

# read and parse the metainfo file (.torrent)
file = open("torrentFiles/Charlie_Chaplin_Mabels_Strange_Predicament.avi.torrent", "rb").read()
torrentt = Torrent.decode(file)

# Connect to tracker to get peers

torrentt.order_trackers()

# print(meta_info.info.piece)
