from threading import Event
from video_stream.video_server import VideoServer

stream_mode = Event()

vs = VideoServer("0.0.0.0", 1337, stream_mode)
vs.start()

# STOP = stream_mode.set()
# START = stream_mode.clear()

running = True
while running:
    # DO STUFF HERE 
    cmd = input("Type: ")
    if cmd == "quit":
        stream_mode.set()
        running = False

