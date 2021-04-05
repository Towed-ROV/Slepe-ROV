import glob
<<<<<<< HEAD
import sys
from time import sleep

import serial as serial
=======
import serial
from time import sleep 
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d


class SerialFinder:
    def __init__(self):
        self.port_name_list = {}
        self.seperation_char = ':'
        self.baud_rate = 0

    def find_com_ports(self):
        """
        Loop through all available com ports on rpi and multiple baud rates.
        :return: dict with all found com ports
        """
        search_runs = 0
        port_names = self.get_available_com_ports()
        print(port_names)
        while search_runs != 2:
            if search_runs == 0:
<<<<<<< HEAD
                self.baud_rate = 57600
            if search_runs == 1:
                self.baud_rate = 115200

            for key in port_names:
                # if 'dev' in key:
                serial_port = serial.Serial(key, self.baud_rate, timeout=1,
                                            stopbits=1, bytesize=8)
                serial_port.write("<reset:True>".encode('utf-8'))
                print(key)
                print(self.baud_rate)
                try:
                    sleep(2)
                    message_received = serial_port.readline()
                    if message_received:
                        print(message_received,'stig')
                        message_received = message_received.strip().decode().split(self.seperation_char)
                        port_name = message_received[0].replace('<', '')
                        if 'IMU' in port_name and self.baud_rate == 57600:
                            self.port_name_list[key] = 'IMU'
                            print('Found IMU')

                        elif 'SensorArduino' in port_name:
                            self.port_name_list[key] = 'SensorArduino'
                            print('Found SensorArduino')
                            print(self.baud_rate)

                        elif 'StepperArduino' in port_name:
                            self.port_name_list[key] = 'StepperArduino'
                            print('Found StepperArduino')
                    serial_port.close()
                    print("serial_port close")
                except (Exception) as e:

                    print(e, 'serial finder')

                    try:
                        serial_port.close()
                    except (Exception) as e:
                        print(e, 'serial finder')
=======
                self.baud_rate = 115200
            if search_runs == 1:
                self.baud_rate = 9600
            if search_runs == 2:
                self.baud_rate = 57600
            if search_runs == 3:
                self.baud_rate = 74880

            for key in port_names:
                if 'dev' in key:
                    serial_port = serial.Serial(key, self.baud_rate, timeout=1,
                                                stopbits=1, bytesize=8)
                    print(key)
                    print(self.baud_rate)
                    try:
                        sleep(2)
                        message_received = serial_port.readline()
                        if message_received:
                            print(message_received,'stig')
                            message_received = message_received.strip().decode().split(self.seperation_char)
                            port_name = message_received[0].replace('<', '')
                            if 'IMU' in port_name and self.baud_rate == 57600:
                                self.port_name_list[key] = 'IMU'
                                print('Found IMU')

                            elif 'SensorArduino' in port_name:
                                self.port_name_list[key] = 'SensorArduino'
                                print('Found SensorArduino')
                                print(self.baud_rate)

                            elif 'StepperArduino' in port_name:
                                self.port_name_list[key] = 'StepperArduino'
                                print('Found StepperArduino')
                        serial_port.close()
                    except (Exception) as e:
                        pass
#                         print(e, 'serial finder')

                        try:
                            serial_port.close()
                        except (Exception) as e:
                            print(e, 'serial finder')
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
            search_runs = search_runs + 1
        print('done')
        return self.port_name_list

    def get_available_com_ports(self):
        """
        find all available com port on rpi
        :return: dict with all com ports on rpi
        """
<<<<<<< HEAD
        # if sys.platform.startswith('win'):
        #     ports = ['COM%s' % (i + 1) for i in range(256)]
        # else:
        #     ports = glob.glob('/dev/tty[A-Za-z]*')
        # port_names = []
        # port_exceptions = ['dev/ttyprintk']
        # i = 0
        # print(ports)
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
        # while i < 3:
        #     for port in ports:
        #         print(port)
        #         if port in ports:
        #             ports.remove(port)
        #     for port in ports:
        #         try:
        #             s = serial.Serial(port, self.baud_rate, timeout=0)
        #             port_names.append(port)
        #
        #         except (OSError, serial.SerialException):
        #             print('errer')
        #         sleep(0.2)
        #     i = i + 1
        #     print(port_names)
        # if not port_names:
        #     print('There are no serial-ports available')
        # port_names = list(dict.fromkeys(port_names))
        # print(port_names)
        # return list(port_names)
=======
        ports = glob.glob('/dev/tty[A-Za-z]*')
        port_names = []
        port_exceptions = ['dev/ttyprintk']
        i = 0
        while i < 3:
            for port in port_exceptions:
                if port in ports:
                    ports.remove(port)
            for port in ports:
                try:
                    s = serial.Serial(port, self.baud_rate, timeout=0)
                    port_names.append(port)
                except (OSError, serial.SerialException):
                    pass
                sleep(0.2)
            i = i + 1
        if not port_names:
            print('There are no serial-ports available')
        port_names = list(dict.fromkeys(port_names))
        return list(port_names)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d





