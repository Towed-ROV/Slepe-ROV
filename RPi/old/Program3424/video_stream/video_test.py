from threading import Event
from video_server import VideoServer

stream_mode = Event()

<<<<<<< HEAD
vs = VideoServer("10.0.0.54", 1337, stream_mode)
=======
vs = VideoServer("192.168.0.102", 1337, stream_mode)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
vs.start()

# STOP = stream_mode.set()
# START = stream_mode.clear()

running = True
while running:
    # Block-free loop
    
    # DO STUFF HERE 
    
    
    cmd = input("Type: ")
    if cmd == "quit":
        stream_mode.set()
        running = False

