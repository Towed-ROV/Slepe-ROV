from time import sleep

import serial

class testser:
    def __init__(self):
        self.serial_port = serial.Serial(
            port='COM27', \
            baudrate=115200, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=0)

        self.count =0

    def send(self):
        self.serial_port.write(("test:" + str(self.count) + "\n").encode('utf-8'))
        self.count = self.count +1
        sleep(0.001)
        print(self.count)
if __name__ == '__main__':
    tets = testser()
    reset = False
    while not reset:
        tets.serial_port.write("SensorArduino:0\n".encode('utf-8'))

        if tets.serial_port.readline().decode('utf-8') == "<reset:True>":
            print("sensor arduino")
            reset = True
        sleep(0.05)
    sleep(5)
    while True:
        tets.send()