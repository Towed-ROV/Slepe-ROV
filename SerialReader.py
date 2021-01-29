import serial
import time
from threading import Thread
class SerialReader(Thread):
    def __init__(self, data, com_port, baud_rate, com_port_value):
        Thread.__init__(self)
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.com_port_value = com_port_value

    def run(self):
        while True:
            try:
                self.read_incomming_data()
            except (Exception)as e:
                print(e)

    def read_incomming_data(self):
        start_char = '<'
        end_char = '>'
        seperation_char = ':'
        serial_port = serial.serial(self.com_port, self.baud_rate, 1)

        if(not serial_port.is_open):
            try:
                serial_port.open()
            except(Exception) as e:
                print(e)
        while True:
            time.sleep(0.05)
            bytes_received = str(serial_port.readline())

            if bytes_received:
                message_received = bytes_received.split(start_char)
                message_received = message_received[1].split(end_char)
                message_received = message_received[0].split(seperation_char)
                return message_received








