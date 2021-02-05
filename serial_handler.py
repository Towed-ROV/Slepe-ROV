from serial_writer import SerialWriter
from serial_reader import SerialReader
from serial_finder import SerialFinder
from sensor import Sensor
from collections import deque
from threading import Thread
class SerialHandler(Thread):
    def __init__(self, message_queue, sensor_list):
        Thread.__init__(self)
        self.reader_queue = deque()
        self.sensor_list = sensor_list
        self.message_queue = message_queue
        self.writer_queue_IMU = deque()
        self.writer_queue_sensor_arudino = deque()
        self.writer_queue_stepper_arduino = deque()
        serial_connected = {}
        self.com_port_found = False


    def run(self):
        if not self.com_port_found:
            self.com_port_found = self.__find_com_ports()
        while self.com_port_found:
            self.__get_incomming_messages()
            self.__write_incomming_messages()
            self.__put_in_writer_queue()

    def __find_com_ports(self):
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list:
            if "IMU" in port_name:
                self.imu_serial_writer = self.__open_writer_thread(self.writer_queue_IMU, com_port, 4800)
                self.imu_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_IMU.append("IMU:OK")
            if "SensorArduino" in port_name:
                self.sensor_arduino_serial_writer = self.__open_writer_thread(self.writer_queue_sensor_arudino,
                                                                              com_port, 4800)
                self.sensor_arduino_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_sensor_arudino.append("sensor_arduino:OK")
            if "StepperArduino" in port_name:
                self.stepper_arduino_serial_writer = self.__open_writer_thread(self.writer_queue_stepper_arduino,
                                                                               com_port, 4800)
                self.stepper_arduino_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_stepper_arduino.append("stepper_arduino:OK")
        return True

    def __write_incomming_messages(self):
        self.imu_serial_writer.put_in_queue(self.writer_queue_IMU)
        self.sensor_arduino_serial_writer.put_in_queue(self.writer_queue_sensor_arudino)
        self.stepper_arduino_serial_writer.put_in_queue(self.writer_queue_stepper_arduino)

    def __get_incomming_messages(self):
        try:
            self.message_queue.append(self.imu_serial_reader.queue.get_nowait())
        except IndexError:
            pass
        try:
            self.message_queue.append(self.sensor_arduino_serial_reader.queue.get_nowait())
        except IndexError:
            pass
        try:
            self.message_queue.append(self.stepper_arduino_serial_reader.queue.get_nowait())
        except IndexError:
            pass
    def set_queue(self, queue):
        self.writer_queue = queue

    def find_com_ports(self):
        serial_finder = SerialFinder
        return serial_finder.find_com_ports()

    def open_reader_thread(self, queue, com_port, baud_rate):
        serial_reader = SerialReader(queue, com_port, baud_rate)
        serial_reader.start()
        return serial_reader

    def __open_writer_thread(self, queue, com_port, baud_rate):
        serial_writer = SerialWriter(queue, com_port, baud_rate)
        serial_writer.start()
        return serial_writer

    def __put_in_writer_queue(self, queue_name):
        item = self.writer_queue.popleft()
        if queue_name == "IMU":
            self.writer_queue_IMU.append(self.writer_queue.popleft())
        elif queue_name == "sensor arduino":
            self.writer_queue_sensor_arudino.append(self.writer_queue.popleft())
        elif queue_name == "stepper arduino":
            self.writer_queue_stepper_arduino.append(self.writer_queue.popleft())

    def test(self, message):
        if message[0] in self.sensor_list.keys():
            sensor = self.sensor_list.value()
            sensor.set_sensor_value(message[1])
        else:
            sensor = Sensor(message[0], message[1])
            self.sensor_list[message[0]] = sensor


if __name__ == "__main__":
    pass