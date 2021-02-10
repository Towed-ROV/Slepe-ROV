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
                print(e, "serialr reader")


    def read_incomming_data(self):
        start_char = '<'
        end_char = '>'
        seperation_char = ':'
        message_received = ""

        if(not self.serial_port.is_open):
            try:
                self.serial_port.open()
            except(Exception) as e:
                print(e, "serial reader")
        while True:
            time.sleep(0.05)
            message_received = self.serial_port.readline()
            message_received = message_received.strip()
            if message_received:
                message_received = message_received.decode().strip(start_char).strip(end_char).split(seperation_char)
                break
        return message_received










