import serial
from threading import Thread
class SerialWriter(Thread):
    def __init__(self, data, com_port, baud_rate):
        Thread.__init__(self)
        self.data = data
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.serial(self.com_port, self.baud_rate, 1)
        self.last_output = ""

    def run(self):
        self.serial_port.open()
        while True:
            try:
                self.write_serial_data()
            except (Exception) as e:
                print(e)

    def write_serial_data(self, message):
        if self.serial_port.open():
            output = "<" + message + ">"
            if output != self.last_output:
                try:
                    self.serial_port.write(output)
                    self.last_output = output
                except (Exception) as e:
                    print(e)
        else:
            print('Serial port not open : ' + str(self.com_port))
