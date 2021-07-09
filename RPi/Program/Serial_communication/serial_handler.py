import threading

from Serial_communication.serial1 import SerialWriterReader
from Serial_communication.serial_finder import SerialFinder
import queue
from multiprocessing import Queue, Process
from threading import Thread
from Serial_communication.handle_writer_queue import HandleWriterQueue
from Serial_communication.serial_message_recived_handler import SerialMessageRecivedHandler
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
        self.writer_queue_IMU = Queue()
        self.writer_queue_sensor_arduino = Queue()
        self.writer_queue_stepper_arduino = Queue()
        self.gui_command_queue = gui_command_queue
        self.serial_connected = []
        self.serial_threads = []
        self.com_port_found = False
        self.VALID_SENSOR_LIST = ['depth', 'pressure', 'temperature',
                                  'wing_pos_port', 'wing_pos_sb',
                                  'yaw', 'roll', 'pitch', 'depth_beneath_rov',
                                  'vertical_acceleration']
        self.serial_message_received_handler = SerialMessageRecivedHandler(self.gui_command_queue, self.sensor_list,
                                                                           self.VALID_SENSOR_LIST, self.reader_queue)
        self.serial_message_received_handler.daemon = True
        self.serial_message_received_handler.start()
        self.handle_writer_queue = HandleWriterQueue(self.reader_queue, self.writer_queue, self.writer_queue_IMU,
                                                     self.writer_queue_sensor_arduino, self.writer_queue_stepper_arduino,
                                                     self.from_arduino_to_arduino_queue,self.VALID_SENSOR_LIST)
    def run(self):
        while True:
            if not self.com_port_found:
                self.__close_threads()
                self.com_port_found = self.__find_com_ports()
                if self.com_port_found:
                    for serial_found in self.serial_connected:
                        self.reader_queue.put(serial_found)
            while self.com_port_found:
                test = self.handle_writer_queue.put_in_writer_queue()
                self.com_port_found = test

#todo active threads list
    def __close_threads(self):
        for thread in self.serial_threads:
            thread.stop_thread()
        self.serial_connected = []
        self.serial_threads = []
        print("serial threads closed")

    def __find_com_ports(self):
        """
        Search for com ports and open serial communication for each port found.
        :return: true if a comport is found and false if not
        """
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list.items():
            if 'IMU' in port_name:
                self.serial_threads.append(self.__open_serial_thread(self.writer_queue_IMU,
                                                                     self.reader_queue, com_port, 57600))
                self.writer_queue_IMU.put('IMU:OK')
                self.serial_connected.append('IMU:'+ com_port)
            if 'SensorArduino' in port_name:
                self.serial_threads.append(self.__open_serial_thread(self.writer_queue_sensor_arduino,
                                                                     self.reader_queue, com_port, 57600))
                self.writer_queue_sensor_arduino.put('sensor_arduino:OK')
                print("ok")
                self.serial_connected.append('SensorArduino:' + com_port)
            if 'StepperArduino' in port_name:
                self.serial_threads.append(self.__open_serial_thread(self.writer_queue_stepper_arduino,
                                                                     self.reader_queue, com_port, 57600))
                self.writer_queue_stepper_arduino.put('stepper_arduino:OK')
                self.serial_connected.append('StepperArduino:' + com_port)
        return True


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
        serial_reader = SerialWriterReader(output_queue, input_queue, com_port, baud_rate,self.from_arduino_to_arduino_queue)
        serial_reader.daemon = True
        serial_reader.start()

        return serial_reader




if __name__ == '__main__':
    pass