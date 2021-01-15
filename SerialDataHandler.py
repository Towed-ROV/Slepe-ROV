import serial
import time
class SerialDataHandler:
    def __init__(self):
        self.portNameList = {}
        self.seperationChar = ":"

    def findComPorts(self):
        baudrate = 0
        searchruns = 0
        portNames = getAv

        while searchruns != 4 :
            if searchruns == 0:
                baudrate = 4800
            if searchruns == 1:
                baudrate = 9600
            if searchruns == 2:
                baudrate = 57600
            if searchruns == 3:
                baudrate = 115200

            for key,value in self.portNamesList.items():
                if value == "Unknown":
                    serialPort = serial.serial(key, baudrate, 1)
                    try:
                        serialPort.Open()
                        time.sleep(5)
                        messageResived = serialPort.readLine()
                        if messageResived:
                            messageResived = messageResived.split(self.seperationChar)
                        if messageResived[0] == "StepperArduino":
                            self.portNamesList[key] = "StepperArduino"
                        serialPort.close()
                    except (Exception) as e:
                        try:
                            serialPort.close()
                        except (Exception) as e:
                            print(e)
            searchruns = searchruns + 1

    def saveComPorts(self):
        comcheck = 0
        for key,value in self.portNameList.items():
            if value != "Unknown":
                data.comPortList[key] = value


    def getAvailableComPorts(self):
        portNames = serial.tools.list_ports.comports()
        if not portNames:
            print("There are no serial-ports available")
        return portNames