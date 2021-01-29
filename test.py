import io
class WorkerRunnable:
    def __init__(self, data, clientSocket):
        self.data = data
        self.sepChar = ":"
        self.clientSocket = clientSocket
        self.bufferSize = 1024

    def run(self):
        clientOnline = True
        try:
            recvMessage = self.clientSocket.recv(self.bufferSize)
            recvMessage = str(recvMessage, 'utf-8').rstrip("\r\n")
            if recvMessage:
                recvMessage = recvMessage.split(self.sepChar)
                cmd = recvMessage[0]
                value = recvMessage[1]
                if cmd:
            else:
                print("no data recived")
        except (Exception) as e:
            print(e)

import glob
import serial
import sys
import time

BAUDRATE = 115200

TIMEOUT = 0

# Create list of potential ports
if sys.platform.startswith('win'):
    ports = ['COM' + str(i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    ports = glob.glob('/dev/tty[A-Za-z]*')
else:
    raise EnvironmentError('Unsupported platform')

port_exceptions = ['dev/ttyprintk']
for port in port_exceptions:
    if port in ports:
        ports.remove(port)

def serial_scanner():
    global ports

    while True:
        for port in ports:
            try:
                s = serial.Serial(port, BAUDRATE, timeout = TIMEOUT, rtscts = 0)
                print('Connected to %s'%port)
            except (OSError, serial.SerialException):
                pass
        time.sleep(1)

if __name__ == '__main__':
    serial_scanner()