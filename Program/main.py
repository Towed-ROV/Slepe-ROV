from Program.payloads.payload_writer import PayloadWriter
from Program.payloads.payload_handler import PayloadHandler
from Program.Serial_communication.serial_handler import SerialHandler
from collections import deque
from threading import Event
from Program.video_stream.video_server import VideoServer

arduino_command_queue = deque()
sensor_list = {}
gui_command_queue = deque()
start1 = 0
#starting threads
payload_writer = PayloadWriter(sensor_list, gui_command_queue)
serial_handler = SerialHandler(sensor_list, arduino_command_queue, gui_command_queue)
payload_handler = PayloadHandler(sensor_list, arduino_command_queue)
payload_handler.daemon = True
payload_handler.start()

#video stream
stream_mode = Event()
vs = VideoServer('0.0.0.0', 1337, stream_mode)
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

def __start_communication_threads():
    try:
        payload_writer.daemon = True
        payload_writer.start()

        serial_handler.daemon = True
        serial_handler.start()
    except (Exception) as e:
        print(e)

def __stop_threads():
    try:
        pass
    except (Exception) as e:
        print(e)

while True:
    try:
        if payload_handler.start1 != 0:
            start_stop_video_stream()
            if payload_handler.start1 == 1 and not(payload_writer.is_alive() or serial_handler.is_alive()):
                print('starting threads')
                __start_communication_threads()
            else:
                __stop_threads()
    except (Exception) as e:
        print(e)