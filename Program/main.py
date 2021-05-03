import threading
from time import sleep
from sea_floor_tracker import SeafloorTracker
from payloads.payload_writer import PayloadWriter
from payloads.payload_handler import PayloadHandler
from Serial_communication.serial_handler import SerialHandler
import queue
from multiprocessing import Event, Queue
# from video_stream.video_server import VideoServer

arduino_command_queue = Queue()
sensor_list = []
gui_command_queue = Queue()
seafloor_sonar_queue = queue.Queue()
flag_queue = queue.Queue()
set_point_queue = Queue()
rov_depth_queue = Queue()

#starting threads
payload_handler = PayloadHandler(sensor_list, arduino_command_queue, gui_command_queue,
                                 seafloor_sonar_queue, flag_queue)
payload_handler.daemon = True
payload_handler.start()

payload_writer = PayloadWriter(sensor_list, gui_command_queue)
serial_handler = SerialHandler(sensor_list, arduino_command_queue, gui_command_queue,
                               set_point_queue, rov_depth_queue)

sea_floor_tracker = SeafloorTracker(150, 20, 20, 6, 10, seafloor_sonar_queue, flag_queue, set_point_queue)


@todo event for start og stop av seafloor tracker
@todo start og stopp av kode


# stream_mode = Event()
# vs = VideoServer('192.168.0.102', 1337, stream_mode)
# vs.daemon = True
# vs.start()
# vs._allow_streaming()

def __start_communication_threads():
    try:
        payload_writer.daemon = True
        payload_writer.start()

        serial_handler.daemon = True
        serial_handler.start()
    except (Exception) as e:
        print(e, ' main')
try:
    if payload_handler.start_rov != False:
        if payload_handler.start_rov == True and not(payload_writer.is_alive() or serial_handler.is_alive()):
            print('starting threads')
            __start_communication_threads()
except (Exception) as e:
    print(e, 'main')
try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    print("exit prg")
