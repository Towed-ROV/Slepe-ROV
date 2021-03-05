from Serial_communication.serial import SerialWriterReader
from Serial_communication.serial_finder import SerialFinder
from collections import deque
from threading import Thread
from handle_writer_queue import HandleWriterQueue
from Serial_communication.serial_message_recived_handler import SerialMessageRecivedHandler
class SerialHandler(Thread):
    def __init__(self, sensor_list, arduino_command_queue, gui_command_queue):
        """

        :param sensor_list: list of all sensor connected
        :param arduino_command_queue: queue storing data that are going to be sent serial
        """
        Thread.__init__(self)
        self.reader_queue = deque()
        self.sensor_list = sensor_list
        self.writer_queue = arduino_command_queue
        self.writer_queue_IMU = deque()
        self.writer_queue_sensor_arduino = deque()
        self.writer_queue_stepper_arduino = deque()
        self.gui_command_queue = deque()
        self.serial_connected = []
        self.com_port_found = False
        self.valid_sensor_list = ['depth', 'pressure', 'temperature',
                                  'stepper_pos_ps', 'stepper_pos_sb',
                                  'yaw', 'roll', 'pitch', 'depth_beneath_rov']
        self.serial_message_received_handler = SerialMessageRecivedHandler(self.gui_command_queue, self.sensor_list, self.valid_sensor_list)
        self.handle_writer_queue = HandleWriterQueue(self.reader_queue,self.writer_queue, self.writer_queue_IMU,
                                              self.writer_queue_sensor_arduino, self.writer_queue_stepper_arduino,
                                                     self.valid_sensor_list)
    def run(self):
        while True:
            if not self.com_port_found:
                self.__close_threads()
                self.com_port_found = self.__find_com_ports()
                if self.com_port_found:
                    for serial_found in self.serial_connected.items():
                        self.serial_message_received_handler.handle_message_recevied(serial_found)
            while self.com_port_found:
                self.__get_incomming_messages()
                test = self.handle_writer_queue.put_in_writer_queue()
                self.com_port_found = test

    def __close_threads(self):
        try:
            self.imu_serial.stop_thread()
        except (Exception) as e:
            print(e)
        try:
            self.sensor_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e)
        try:
            self.stepper_arduino_serial_writer.stop_thread()
        except (Exception) as e:
            print(e)

    def __find_com_ports(self):
        """
        Search for com ports and open serial communication for each port found.
        :return: true if a comport is found and false if not
        """
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list.items():
            if 'IMU' in port_name:
                self.imu_serial = self.__open_serial_thread(self.writer_queue_IMU, self.reader_queue, com_port, 4800)
                self.writer_queue_IMU.append('IMU:OK')
                self.serial_connected.append('IMU:'+ com_port)
            if 'SensorArduino' in port_name:
                self.sensor_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_sensor_arduino,
                                                                              self.reader_queue, com_port, 4800)
                self.writer_queue_sensor_arduino.append('sensor_arduino:OK')
                self.serial_connected.append('SensorArduino:' + com_port)
            if 'StepperArduino' in port_name:
                self.stepper_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_stepper_arduino,
                                                                               self.reader_queue, com_port, 4800)
                self.writer_queue_stepper_arduino.append('stepper_arduino:OK')
                self.serial_connected.append('StepperArduino' + com_port)
        return True

    def __get_incomming_messages(self):
        """
        Takes first message read from serial and pass it on to message queue.
        Also checks if the message is a sensor, and either update the sensor value or add a new sensor.
        """
        try:
            message = self.reader_queue.popleft()
            self.serial_message_received_handler.handle_message_recevied(message)
        except IndexError:
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
        serial_reader = SerialWriterReader(output_queue, input_queue, com_port, baud_rate)
        serial_reader.daemon = True
        serial_reader.start()
        return serial_reader




if __name__ == '__main__':
    pass