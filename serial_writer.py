import serial
import time
from threading import Thread
class SerialWriter(Thread):
    def __init__(self, queue, com_port, baud_rate):
        Thread.__init__(self)
        self.queue = queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=0)
        self.last_output = ""
        self.message_to_send = ""

    def run(self):
        self.serial_port.open()
        while True:
            try:
                self.__write_serial_data(self.queue.popleft())
            except (Exception) as e:
                print(e)

    def __write_serial_data(self):
        if self.serial_port.isOpen():
            output = "<" + self.message_to_send + ">"

            if output != "self.last_output":

                try:
                    out = output.encode('utf-8')
                    print(out)
                    self.serial_port.write(out)
                    self.last_output = output
                    self.serial_port.close()
                except (Exception) as e:
                    print(e)
        else:
            self.serial_port.open()
            print('Serial port not open : ' + str(self.com_port))

    def put_in_queue(self, item):
        self.queue.append(item)
        return True



if __name__ == "__main__":
    ser = SerialWriter('com8', 4800)
    while True:
        ser.write_serial_data("test:1")
        time.sleep(1)
