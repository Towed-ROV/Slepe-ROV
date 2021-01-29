import glob

import serial
import time
import serial.tools.list_ports
class SerialFinder:
    def __init__(self):
        self.port_name_list = {}
        self.seperation_char = ":"

    def find_com_ports(self):
        search_runs = 0
        self.port_names = self.get_available_com_ports()
        print(self.port_names)
        while search_runs != 4:
            if search_runs == 0:
                self.baud_rate = 4800
            if search_runs == 1:
                self.baud_rate = 9600
            if search_runs == 2:
                self.baud_rate = 57600
            if search_runs == 3:
                self.baud_rate = 115200
            for key in self.port_names:
                if 'dev' in key:
                    serial_port = serial.Serial(key, self.baud_rate, timeout=0, rtscts=0)
                    print(key)
                    try:
                        serial_port.Open()
                        time.sleep(5)
                        message_resived = serial_port.readLine()
                        if message_resived:
                            message_resived = message_resived.split(self.seperation_char)
                        if message_resived[0] == "StepperArduino":
                            self.port_name_list[key] = "StepperArduino"
                        serial_port.close()
                    except (Exception) as e:
                        try:
                            serial_port.close()
                        except (Exception) as e:
                            print(e)
            search_runs = search_runs + 1

    def get_available_com_ports(self):
        ports = glob.glob('/dev/tty[A-Za-z]*')
        port_names = []
        port_exceptions = ['dev/ttyprintk']
        i = 0
        while i < 3:
            for port in port_exceptions:
                if port in ports:
                    print(port)
                    ports.remove(port)
            for port in ports:
                try:
                    s = serial.Serial(port, self.baud_rate, timeout=0, rtscts=0)
                    port_names.append(port)
                except (OSError, serial.SerialException):
                    pass
                time.sleep(1)
            i = i + 1
        if not port_names:
            print("There are no serial-ports available")
        port_names = list(dict.fromkeys(port_names))
        return list(port_names)

if __name__ == "__main__":
    serial_finder = SerialFinder

    print(serial_finder.get_available_com_ports())

import glob

import serial
import time
import serial.tools.list_ports




                    try:
                        print('1')

                        print('2')
                        time.sleep(5)
                        print('3')
                        for c in serialPort.read():
                            line.append(c)
                            if c == '\n':
                                print("Line: " + ''.join(line))
                                line = []
                                break

                        print(messageResived)
                        if messageResived:
                            messageResived = messageResived.split(self.seperationChar)
                        if messageResived[0] == "IMU":
                            self.port_name_list[key] = "IMU"
                            print('found imu')
                        serialPort.close()
                    except (Exception) as e:
                        print(e)
                        try:
                            serialPort.close()
                        except (Exception) as e:
                            print(e)
            searchruns = searchruns + 1




if __name__ == "__main__":
    serialFinder = SerialFinder()
    serialFinder.find_com_ports()