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
        self.stop = False

    def run(self):
        while not False:
            try:
                incomming_message = self.__read_incomming_data()
                if incomming_message:
                    self.input_queue.append(incomming_message)
                test = self.output_queue.popleft()
                self.__write_serial_data(test)
                
            except (Exception) as e:
                pass

    def __write_serial_data(self, message):
        """
        write message to serial port
        :param message: message to send to serial
        """
        if self.serial_port.isOpen():
            output = '<' + message + '>'
            if output != 'self.last_output':

                try:
                    output = output.encode()
                    self.serial_port.write(output)
                    time.sleep(0.05)
                    self.last_output = output
                except (Exception) as e:
                    print(e, 'serial writer')
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
        message_received = ''
        try:
            message_received = self.serial_port.readline()
            message_received = message_received.strip()
            message_received = message_received.decode('utf-8').strip(start_char).strip(end_char)
            return message_received
        except (Exception) as e:
            pass
        
    def stop_thread(self):
        self.stop = True
        self.serial_port.close()
        print('closed port', self.serial_port.isOpen())
        