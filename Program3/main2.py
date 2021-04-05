from payloads.payload_writer import PayloadWriter
from payloads.payload_handler import PayloadHandler
from Serial_communication.serial_handler import SerialHandler
from collections import deque
from threading import Event
from video_stream.video_server import VideoServer

command_queue = deque()
sensor_list = {}
message_queue = deque()

#starting threads
payload_handler = PayloadHandler(sensor_list, command_queue)
payload_handler.daemon = True
payload_handler.start()

payload_writer = PayloadWriter(sensor_list)
payload_writer.daemon = True
payload_writer.start()

serial_handler = SerialHandler(sensor_list, command_queue)
serial_handler.daemon = True
serial_handler.start()

#video stream
stream_mode = Event()
vs = VideoServer("0.0.0.0", 1337, stream_mode)
vs.start()

def start_stop_video_stream():
    try: 
        command_data = command_queue.popleft()
        command_queue.appendleft(command_data)
        command_data = command_data.split(':',1)
        command_name = command_data[0]
        if command_name == 'stop_video_stream':
            vs._stop_streaming()
        if command_name == 'start_video_stream':
            vs._allow_streaming()
    except IndexError:
        pass

while True:
    start_stop_video_stream()
