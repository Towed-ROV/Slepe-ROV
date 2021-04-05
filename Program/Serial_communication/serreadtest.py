from threading import Thread

import serial


class readTest(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.serial_port = serial.Serial(
            port='COM28', \
            baudrate=115200, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=0)

    def read(self):
        msg = self.serial_port.read(self.serial_port.in_waiting)
        if msg:
            msg = msg.decode('utf-8')
        return msg

if __name__ == '__main__':
    tets = readTest()
    tets.daemon = True
    tets.start()
    while True:
        pass