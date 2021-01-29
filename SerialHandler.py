import serial
import time
import SerialFinder
import SerialReader
import SerialWriter
import threading
from threading import Thread
class SerialHandler:
    def __init__(self):
        serial_connected = {}
    def find_com_ports(self):
        serial_finder = SerialFinder
        serial_connected = serial_finder.find_com_ports()
    def open_reader_thread(self):
        serial_reader = SerialReader()
        serial_reader.start()