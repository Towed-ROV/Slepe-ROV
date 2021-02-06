from payload_writer import PayloadWriter
from payload_handler import PayloadHandler
from serial_handler import SerialHandler
from collections import deque

command_queue = deque()
sensor_list = []
message_queue = deque()

#starting threads
payload_handler = PayloadHandler(command_queue)
payload_handler.daemon = True
payload_handler.start()

payload_writer = PayloadWriter(sensor_list)
payload_writer.daemon = True
payload_writer.start()

serial_handler = SerialHandler(command_queue, sensor_list)
serial_handler.daemon = True
serial_handler.start()



