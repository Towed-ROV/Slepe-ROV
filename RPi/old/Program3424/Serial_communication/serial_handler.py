from Serial_communication.serial1 import SerialWriterReader
from Serial_communication.serial_finder import SerialFinder
<<<<<<< HEAD
import queue
from multiprocessing import Queue
from threading import Thread
from Serial_communication.handle_writer_queue import HandleWriterQueue
from Serial_communication.serial_message_recived_handler import SerialMessageRecivedHandler


=======
from collections import deque
from threading import Thread
from Serial_communication.handle_writer_queue import HandleWriterQueue
from Serial_communication.serial_message_recived_handler import SerialMessageRecivedHandler
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
class SerialHandler(Thread):
    def __init__(self, sensor_list, arduino_command_queue, gui_command_queue):
        """

        :param sensor_list: list of all sensor connected
        :param arduino_command_queue: queue storing data that are going to be sent serial
        """
        Thread.__init__(self)
        self.from_arduino_to_arduino_queue = Queue()
        self.reader_queue = Queue()
        self.sensor_list = sensor_list
        self.writer_queue = arduino_command_queue
<<<<<<< HEAD
        self.writer_queue_IMU = Queue()
        self.writer_queue_sensor_arduino = Queue()
        self.writer_queue_stepper_arduino = Queue()
=======
        self.writer_queue_IMU = deque()
        self.writer_queue_sensor_arduino = deque()
        self.writer_queue_stepper_arduino = deque()
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        self.gui_command_queue = gui_command_queue
        self.serial_connected = []
        self.com_port_found = False
        self.valid_sensor_list = ['depth', 'pressure', 'temperature',
                                  'wing_pos_port', 'wing_pos_sb',
<<<<<<< HEAD
                                  'yaw', 'roll', 'pitch', 'depth_beneath_rov',
                                  'velocity_vertical']
        self.serial_message_received_handler = SerialMessageRecivedHandler(self.gui_command_queue, self.sensor_list, self.valid_sensor_list)
        self.handle_writer_queue = HandleWriterQueue(self.reader_queue,self.writer_queue, self.writer_queue_IMU,
                                              self.writer_queue_sensor_arduino, self.writer_queue_stepper_arduino,
                                                     self.from_arduino_to_arduino_queue)
=======
                                  'yaw', 'roll', 'pitch', 'depth_beneath_rov']
        self.serial_message_received_handler = SerialMessageRecivedHandler(self.gui_command_queue, self.sensor_list, self.valid_sensor_list)
        self.handle_writer_queue = HandleWriterQueue(self.reader_queue,self.writer_queue, self.writer_queue_IMU,
                                              self.writer_queue_sensor_arduino, self.writer_queue_stepper_arduino)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
    def run(self):
        while True:
            if not self.com_port_found:
                self.__close_threads()
                self.com_port_found = self.__find_com_ports()
                if self.com_port_found:
                    for serial_found in self.serial_connected:
                        self.serial_message_received_handler.handle_message_recevied(serial_found)
            while self.com_port_found:
                self.__get_incomming_messages()
                test = self.handle_writer_queue.put_in_writer_queue()
                self.com_port_found = test

    def __close_threads(self):
        try:
            self.imu_serial.stop_thread()
        except (Exception) as e:
<<<<<<< HEAD
            print(e,'SH')
        try:
            self.sensor_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e,'SH')
        try:
            self.stepper_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e,'SH')
=======
            print(e)
        try:
            self.sensor_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e)
        try:
            self.stepper_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d

    def __find_com_ports(self):
        """
        Search for com ports and open serial communication for each port found.
        :return: true if a comport is found and false if not
        """
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list.items():
            if 'IMU' in port_name:
<<<<<<< HEAD
                self.imu_serial = self.__open_serial_thread(self.writer_queue_IMU, self.reader_queue, com_port, 57600)
                self.writer_queue_IMU.put('IMU:OK')
=======
                self.imu_serial = self.__open_serial_thread(self.writer_queue_IMU, self.reader_queue, com_port, 56700)
                self.writer_queue_IMU.append('IMU:OK')
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
                self.serial_connected.append('IMU:'+ com_port)
            if 'SensorArduino' in port_name:
                self.sensor_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_sensor_arduino,
                                                                              self.reader_queue, com_port, 115200)
<<<<<<< HEAD
                self.writer_queue_sensor_arduino.put('sensor_arduino:OK')
                self.serial_connected.append('SensorArduino:' + com_port)
            if 'StepperArduino' in port_name:
                self.stepper_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_stepper_arduino,
                                                                               self.reader_queue, com_port, 57600)
                self.writer_queue_stepper_arduino.put('stepper_arduino:OK')
=======
                self.writer_queue_sensor_arduino.append('sensor_arduino:OK')
                self.serial_connected.append('SensorArduino:' + com_port)
            if 'StepperArduino' in port_name:
                self.stepper_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_stepper_arduino,
                                                                               self.reader_queue, com_port, 74880)
                self.writer_queue_stepper_arduino.append('stepper_arduino:OK')
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
                self.serial_connected.append('StepperArduino:' + com_port)
        return True

    def __get_incomming_messages(self):
        """
        Takes first message read from serial and pass it on to message queue.
        Also checks if the message is a sensor, and either update the sensor value or add a new sensor.
        """
        try:
<<<<<<< HEAD
            message = self.reader_queue.get_nowait()
#             print(message)
            self.serial_message_received_handler.handle_message_recevied(message)
        except queue.Empty:
=======
            message = self.reader_queue.popleft()
#             print(message)
            self.serial_message_received_handler.handle_message_recevied(message)
        except IndexError:
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
            pass

    def find_com_ports(self):
        """
        Search for com ports
        :return: dict of found com ports
        """
        serial_finder = SerialFinder()
        return serial_finder.find_com_ports()

    def __open_serial_thread(self, output_queue, input_queue, com_port, baud_rate):
        """
        Open thread for serial communication
        :param output_queue: a queue with messages to write serial
        :param input_queue: a queue with messages read from serial
        :param com_port: the com port of the serial port
        :param baud_rate: the baud rate for the serial communication
        :return:
        """
<<<<<<< HEAD
        serial_reader = SerialWriterReader(output_queue, input_queue, com_port,
                                           baud_rate, self.from_arduino_to_arduino_queue)
=======
        serial_reader = SerialWriterReader(output_queue, input_queue, com_port, baud_rate)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        serial_reader.daemon = True
        serial_reader.start()
        return serial_reader




if __name__ == '__main__':
    pass