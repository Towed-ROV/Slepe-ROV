from threading import Thread
import serial
import queue

ENCODING = 'utf-8'
TERMINATOR = ':'
START_CHAR = '<'
END_CHAR = '>'

class SerialWriterReader(Thread):
    def __init__(self, output_queue, input_queue, com_port, baud_rate, from_arduino_to_arduino_queue):
        Thread.__init__(self)
        self.from_arduino_to_arduino_queue = from_arduino_to_arduino_queue
        self.output_queue = output_queue
        self.input_queue = input_queue
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(
            port=self.com_port,\
            baudrate=self.baud_rate,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
        self.stop = False
        self.last_output = ''
        self.FROM_ARDUINO_TO_ARDUINO = ['depth', 'roll', 'pitch']
        self.counter = 0

    def run(self):
        while True:
            try:
                test = self.output_queue.get_nowait()
                self.__write_serial_data(test)
            except queue.Empty:
                pass
            except TypeError:
                pass
            incoming_message = self.__read_incoming_data()
            for message in incoming_message:
                if message:
                    # print(message)
                    try:
                        self.input_queue.put_nowait(message)
                        msg = message.split(TERMINATOR,1)[0]
                        if msg in self.FROM_ARDUINO_TO_ARDUINO:
                            # print(message,'kuk')
                            try:
                                self.from_arduino_to_arduino_queue.put(message)
                            except queue.Full:
                                pass
                    except queue.Full:
                        pass

    def __write_serial_data(self, message):
        """
        write message to serial port
        :param message: message to send to serial
        """
        if self.serial_port.isOpen():
            output = START_CHAR + message + END_CHAR
            if output != self.last_output:
                try:
                    output = output.encode(ENCODING)
                    self.serial_port.write(output)
                    # print(output, '    ', str(self.COUNTER), '    ', self.baud_rate)
                    # self.COUNTER = self.COUNTER +1
                    self.last_output = output
                except (Exception) as e:
                    print(e, 'serial writer')
        else:
            self.serial_port.open()
            print('Serial port not open : ' + str(self.com_port))
            self.output_queue.append(message)

    def __read_incoming_data(self):
        """
        reads from serial port
        :return: message read from serial port
        """
        message_received = ""
        try:
            message_received = self.serial_port.read(self.serial_port.in_waiting or 1)

            message_received = message_received.decode(ENCODING).\
                                                replace(START_CHAR, "").\
                                                replace(END_CHAR, "").\
                                                replace(" ", "")
            message_received = message_received.split("\n")
            # if message_received:
            #     print(message_received, "e de sammenheng")
        except (Exception) as e:
            print(e, "serial1")
        return message_received

    def stop_thread(self):
        self.stop = True
        self.serial_port.close()
        print('closed port', self.serial_port.isOpen())
        
if __name__ == '__main__':
    q1 = queue.Queue()
    q2 = queue.Queue()
    q3 = queue.Queue()
    ser = SerialWriterReader(q1,q2,'COM28', 115200, q3)
    ser.daemon =  True
    ser.start()
    while True:
        pass