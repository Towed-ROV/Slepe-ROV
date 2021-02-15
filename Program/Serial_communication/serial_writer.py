import serial
import time
from threading import Thread
class SerialWriter(Thread):
    def __init__(self, queue, com_port, baud_rate):
        Thread.__init__(self)
        self.queue = queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=0,
                                         stopbits=1, bytesize=8)
        self.last_output = ""

    def run(self):
        while True:
            try:
                test = self.queue.popleft()
                print(test)
                self.__write_serial_data(test)
            except (Exception) as e:
                pass






if __name__ == "__main__":
    ser = SerialWriter('com8', 4800)
    while True:
        ser.write_serial_data("test:1")
        time.sleep(1)
