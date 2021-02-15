import serial
import time
from threading import Thread
class SerialWriterReader(Thread):
    def __init__(self, output_queue, input_queue, com_port, baud_rate):
        Thread.__init__(self)
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=0,
                                         stopbits=1, bytesize=8)
        self.last_output = ''

    def run(self):
        while True:
            try:
                self.input_queue.append(self.__read_incomming_data())
                self.__write_serial_data(self.output_queue.popleft())
            except (Exception) as e:
                pass

    def __write_serial_data(self, message):
        """
        write message to serial port
        :param message: message to send to serial
        """
        if self.serial_port.isOpen():
            output = "<" + message + ">"
            print(message)
            if output != "self.last_output":

                try:
                    out = output.encode('utf-8')
                    print("shit")
                    print(out)
                    self.serial_port.write(out)
                    self.last_output = output
                    self.serial_port.close()
                except (Exception) as e:
                    print(e, "serial writer")
        else:
            self.serial_port.open()
            print('Serial port not open : ' + str(self.com_port))
            self.queue.appendleft(message)

    def __read_incomming_data(self):
        """
        reads from serial port
        :return: message read from serial port
        """
        start_char = '<'
        end_char = '>'
        seperation_char = ':'
        message_received = ""

        if(not self.serial_port.is_open):
            try:
                self.serial_port.open()
            except(Exception) as e:
                print(e, "serial reader")
        while True:
            time.sleep(0.05)
            message_received = self.serial_port.readline()
            message_received = message_received.strip()
            if message_received:
                print(message_received)
                message_received = message_received.decode().strip(start_char).strip(end_char).split(seperation_char)
                break
        return message_received