from Serial_communication.serial import SerialWriterReader
from Serial_communication.serial_finder import SerialFinder
from sensor import Sensor
from collections import deque
from threading import Thread
from handle_writer_queue import HandleWriterQueue
class SerialHandler(Thread):
    def __init__(self, sensor_list, writer_queue):
        """

        :param sensor_list: list of all sensor connected
        :param writer_queue: queue storing data that are going to be sent serial
        """
        Thread.__init__(self)
        self.reader_queue = deque()
        self.sensor_list = sensor_list
        self.message_queue = deque()
        self.writer_queue = writer_queue
        self.writer_queue_IMU = deque()
        self.writer_queue_sensor_arduino = deque()
        self.writer_queue_stepper_arduino = deque()
        self.serial_connected = {}
        self.com_port_found = False
        self.handle_writer_queue = HandleWriterQueue(self.reader_queue,self.writer_queue, self.writer_queue_IMU,
                                              self.writer_queue_sensor_arduino, self.writer_queue_stepper_arduino)

    def run(self):
        if not self.com_port_found:
            self.com_port_found = self.__find_com_ports()
        while self.com_port_found:
            self.__get_incomming_messages()
            self.com_port_found = self.handle_writer_queue.put_in_writer_queue(self.com_port_found)
            
    def __find_com_ports(self):
        """
        Search for com ports and open serial communication for each port found.
        :return: true if a comport is found and false if not
        """
        com_port_found = False
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list.items():
            if "IMU" in port_name:
                self.imu_serial = self.__open_serial_thread(self.writer_queue_IMU, self.reader_queue, com_port, 4800)
                self.writer_queue_IMU.append("IMU:OK")
                self.serial_connected["IMU"]= com_port
                com_port_found = True
            if "SensorArduino" in port_name:
                self.sensor_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_sensor_arduino,
                                                                              self.reader_queue, com_port, 4800)
                self.writer_queue_sensor_arduino.append("sensor_arduino:OK")
                self.serial_connected["SensorArduino"]= com_port
                com_port_found = True
            if "StepperArduino" in port_name:
                self.stepper_arduino_serial_writer = self.__open_serial_thread(self.writer_queue_stepper_arduino,
                                                                               self.reader_queue, com_port, 4800)
                self.writer_queue_stepper_arduino.append("stepper_arduino:OK")
                self.serial_connected["StepperArduino"]= com_port
                com_port_found = True
        return com_port_found

    def __get_incomming_messages(self):
        """
        Takes first message read from serial and pass it on to message queue.
        Also checks if the message is a sensor, and either update the sensor value or add a new sensor.
        """
        try:
            message = self.reader_queue.popleft()
            self.message_queue.append(message)
            self.__add_sensor(message)
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

    def __add_sensor(self, message):
        """
        checks of message is an expected on, and if, it adds the message/sensor to the list of sensors.
        If the sensor is already in the list it updates it's value.
        :param message:
        """
        if ("IMU" or "sensorArduino" or "stepperArduino") in message[0]:
            pass
        else:
            if message[0] == ("depth" or "pressure" or "temperature"
            or "stepper_pos_ps" or "stepper_pos_sb" or "yaw" or "roll"
            or "pitch" or "depth_beneath_rov") :
                if message[0] in self.sensor_list.keys():
                    self.sensor_list[message[0]] = message[1]
                else:
                    sensor = Sensor(message[0], message[1])
                    # print('------')
                    # print(sensor)
                    # print('------')
                    self.sensor_list[message[0]] = sensor


if __name__ == "__main__":
    pass