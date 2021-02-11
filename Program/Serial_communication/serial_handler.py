from Serial_communication.serial_writer import SerialWriter
from Serial_communication.serial_reader import SerialReader
from Serial_communication.serial_finder import SerialFinder
from sensor import Sensor
from collections import deque
from threading import Thread
from handle_writer_queue import HandleWriterQueue
class SerialHandler(Thread):
    def __init__(self, sensor_list, writer_queue):
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
            self.handle_writer_queue.put_in_writer_queue()

    def __find_com_ports(self):
        com_port_found = False
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list.items():
            if "IMU" in port_name:
                self.imu_serial_writer = self.__open_writer_thread(self.writer_queue_IMU, com_port, 4800)
                self.imu_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_IMU.append("IMU:OK")
                self.serial_connected["IMU"]= com_port
                com_port_found = True
            if "SensorArduino" in port_name:
                self.sensor_arduino_serial_writer = self.__open_writer_thread(self.writer_queue_sensor_arduino,
                                                                              com_port, 4800)
                self.sensor_arduino_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_sensor_arduino.append("sensor_arduino:OK")
                self.serial_connected["SensorArduino"]= com_port
                com_port_found = True
            if "StepperArduino" in port_name:
                self.stepper_arduino_serial_writer = self.__open_writer_thread(self.writer_queue_stepper_arduino,
                                                                               com_port, 4800)
                self.stepper_arduino_serial_reader = self.open_reader_thread(self.reader_queue, com_port, 4800)
                self.writer_queue_stepper_arduino.append("stepper_arduino:OK")
                self.serial_connected["StepperArduino"]= com_port
                com_port_found = True
        return com_port_found

    def __get_incomming_messages(self):
        try:
            test = self.reader_queue.popleft()
            self.message_queue.append(test)
            self.__add_sensor(test)
        except IndexError:
            pass

    def find_com_ports(self):
        serial_finder = SerialFinder()
        return serial_finder.find_com_ports()

    def open_reader_thread(self, queue, com_port, baud_rate):
        serial_reader = SerialReader(queue, com_port, baud_rate)
        serial_reader.daemon = True
        serial_reader.start()
        return serial_reader

    def __open_writer_thread(self, queue, com_port, baud_rate):
        serial_writer = SerialWriter(queue, com_port, baud_rate)
        serial_writer.daemon = True
        serial_writer.start()
        return serial_writer

    def __add_sensor(self, message):
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
                    print('------')
                    print(sensor)
                    print('------')
                    self.sensor_list[message[0]] = sensor


if __name__ == "__main__":
    pass