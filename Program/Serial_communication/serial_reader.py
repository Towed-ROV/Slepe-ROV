import serial
import time
from threading import Thread
class SerialReader(Thread):
    def __init__(self, queue, com_port, baud_rate):
        Thread.__init__(self)
        self.queue = queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=0)
        self.message_received = ""
    def run(self):
        while True:
            try:
                self.queue.append(self.read_incomming_data())
            except (Exception)as e:
                pass
                print(e, "serial reader")













