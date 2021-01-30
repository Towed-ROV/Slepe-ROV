import serial
import time
import threading
from serial_writer import SerialWriter
from threading import Thread
class SerialHandler:
    def __init__(self):
        serial_connected = {}
        com_ports_list = self.find_com_ports()
        for com_port, port_name in com_ports_list:
            if "IMU" in port_name:
                self.open_writer_thread(com_port, 4800)
                self.open_reader_thread(com_port, 4800)
            if "SensorArduino" in port_name:
                self.open_writer_thread(com_port, 4800)
                self.open_reader_thread(com_port, 4800)
            if "StepperArduino" in port_name:
                self.open_writer_thread(com_port, 4800)
                self.open_reader_thread(com_port, 4800)
    def find_com_ports(self):
        serial_finder = SerialFinder
        return serial_finder.find_com_ports()
    def open_reader_thread(self, com_port, baud_rate):
        serial_reader = SerialReader(com_port, baud_rate)
        serial_reader.start()
    def open_writer_thread(self, com_port, baud_rate):
        serial_writer = SerialWriter(com_port, baud_rate)
        serial_writer.start()
        return serial_writer

if __name__ == "__main__":
    Serialhandler = SerialHandler()