from payloads.payload_writer import PayloadWriter
from payloads.payload_handler import PayloadHandler
from Serial_communication.serial_handler import SerialHandler
import queue
from multiprocessing import Event, Queue
from video_stream.video_server import VideoServer

arduino_command_queue = Queue()
sensor_list = {}
gui_command_queue = Queue()
#starting threads
payload_writer = PayloadWriter(sensor_list, gui_command_queue)
serial_handler = SerialHandler(sensor_list, arduino_command_queue, gui_command_queue)
payload_handler = PayloadHandler(sensor_list, arduino_command_queue, gui_command_queue)
payload_handler.daemon = True
payload_handler.start()




# stream_mode = Event()
# vs = VideoServer('10.0.0.54', 1337, stream_mode)
# vs.start()
# # vs._allow_streaming()

def __start_communication_threads():
    try:
        payload_writer.daemon = True
        payload_writer.start()

        serial_handler.daemon = True
        serial_handler.start()
    except (Exception) as e:
        print(e, ' main')


while True:
    try:
        if payload_handler.start_rov != False:
            if payload_handler.start_rov == True and not(payload_writer.is_alive() or serial_handler.is_alive()):
                print('starting threads')
                __start_communication_threads()
    except (Exception) as e:
        print(e, 'main')