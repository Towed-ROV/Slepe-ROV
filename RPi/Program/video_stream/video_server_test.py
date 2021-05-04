from threading import Event
from video_server import VideoServer

stream_mode = Event()

vs = VideoServer("192.168.0.102", 1339, stream_mode)
vs.daemon = True
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

