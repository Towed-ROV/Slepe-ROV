import pickle
import struct

""" Helper methods for the sockets """


def process_frame(frame_bytes):
    data = pickle.dumps(frame_bytes, 0)
    size = len(data)
    return struct.pack(">L", size) + data
