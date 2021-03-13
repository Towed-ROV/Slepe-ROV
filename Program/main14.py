from threading import Event
from video_stream.video_server import VideoServer

stream_mode = Event()
vs = VideoServer('192.168.0.102', 1337, stream_mode)
vs.start()

def start_stop_video_stream():
    try: 
        command_data = arduino_command_queue.popleft()
        arduino_command_queue.appendleft(command_data)
        command_data = command_data.split(':',1)
        command_name = command_data[0]
        if command_name == 'stop_video_stream':
            vs._stop_streaming()
        if command_name == 'start_video_stream':
            vs._allow_streaming()
    except IndexError:
        pass
