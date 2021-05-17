import serial
import queue
from threading import Thread
from time import time

ENCODING = 'utf-8'
TERMINATOR = ':'
START_CHAR = '<'
END_CHAR = '>'
NEW_LINE = '\n'
START = b'<'
STOP = b'>'


class SerialWriterReader(Thread):
    """
    Serial reader and writer running as a thread to read and write data to and from a serial port.
    """
    def __init__(self, output_queue, input_queue, com_port, baud_rate, from_arduino_to_arduino_queue):
        Thread.__init__(self)
        self.from_arduino_to_arduino_queue = from_arduino_to_arduino_queue
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(
            port=self.com_port,
            baudrate=self.baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0)
        self.stop = False
        self.in_packet = bytearray()
        self.packet = bytearray()
        self.last_output = ''
        self.FROM_ARDUINO_TO_ARDUINO = ['depth', 'roll', 'pitch']

    def run(self):
        """
        Threaded run function that checks if there are message to be sent, sends message.
        Followed by reading the input for data, put the received data in a queue to be processed elsewhere.

        """
        while not self.stop:
            try:
                test = self.output_queue.get(timeout=0.001)
                self.__write_serial_data(test)
            except queue.Empty:
                pass
            except TypeError:
                pass
            incoming_message = self.__read_incoming_data()
            for message in incoming_message:
                if message:
                    try:
                        if not "Arduino" in message:
                            print(message)
                            try:
                                self.input_queue.put_nowait(message)
                                msg = message.split(TERMINATOR, 1)[0]
                                if msg in self.FROM_ARDUINO_TO_ARDUINO:
                                    try:
                                        self.from_arduino_to_arduino_queue.put_nowait(message)
                                    except queue.Full:
                                        pass
                            except queue.Full:
                                pass
                    except TypeError:
                        pass

    def __write_serial_data(self, message):
        """
        Write message to serial port
        :param message: message to send to serial
        """
        if self.serial_port.isOpen():
            output = START_CHAR + message + END_CHAR + NEW_LINE
            if output != self.last_output:
                try:
                    output = output.encode(ENCODING)
                    self.serial_port.write(output)
                    self.last_output = output
                except (Exception) as e:
                    print(e, 'serial writer')
        else:
            self.serial_port.open()
            print('Serial port not open : ' + str(self.com_port))
            self.output_queue.append(message)

    def handle_packet(self, data):
        """
        Decodes data and removes charaters
        @param data: Bytes received for the serial port
        @return: the decoded data as a string.
        """
        message_received = data.decode(ENCODING). \
            replace(START_CHAR, ""). \
            replace(END_CHAR, ""). \
            replace(" ", "")
        return message_received

    def __read_incoming_data(self):
        """
        Reads from serial port, iterates over each byte to find the start byte "<" and add each follow byte to a
        variable of bytes until the byte received equal the stop byte ">". The bytes will be decoded and a string of
         received data will be returned
        :return: message(String) read from serial port
        """
        data_received = []
        message_received = ""
        try:
            data = self.serial_port.read(self.serial_port.in_waiting or 1)
            for byte in serial.iterbytes(data):
                if byte == START:
                    self.in_packet = True
                elif byte == STOP:
                    self.in_packet = False
                    data_received.append(self.handle_packet(bytes(self.packet)))  # make read-only copy
                    del self.packet[:]
                elif self.in_packet:
                    self.packet.extend(byte)
                else:
                    pass

        except (Exception) as e:
            print(e, "serial1")
        return data_received

    def stop_thread(self):
        self.stop = True
        self.serial_port.close()
        print('closed port', self.serial_port.isOpen())

