import serial
import time
class ReadSerialData:
    def __init__(self, data, comPort, baudRate, comPortValue):
        self.data = data
        self.comport = comPort
        self.baudRate = baudRate
        self.comPortValue = comPortValue

    def run(self):
        while True:
            try:
                self.readIncommingData()
            except (Exception)as e:
                print(e)

    def readIncommingData(self):
        startChar = '<'
        endChar = '>'
        seperationChar = ':'
        serialPort = serial.serial(self.comPort, self.baudRate, 1)

        if(not serialPort.is_open):
            try:
                serialPort.open()
            except(Exception) as e:
                print(e)
        while True:
            time.sleep(0.05)
            bytesResived = str(serialPort.readline())

            if bytesResived:
                messageResived = bytesResived.split(startChar)
                messageResived = messageResived[1].split(endChar)
                messageResived = messageResived[0].split(seperationChar)
                self.IncommingDataHandler(messageResived)

    def IncommingDataHandler(self, messageResived):
        key = messageResived[0]
        message = messageResived[1]
        if key == 1:
        elif key == 2:






