import serial
import time
import queue
from multiprocessing import Process, Queue
class SerialWriterReader(Process):
    def __init__(self, output_queue, input_queue, com_port, baud_rate, from_arduino_to_arduino_queue):
        Process.__init__(self)
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
        self.last_output = ''
        self.stop = False
        self.from_arduino_to_arduino = ['depth','roll','pitch']
        self.counter =0

    def run(self):
        while not self.stop:
            try:
                test = self.output_queue.get_nowait()
                self.__write_serial_data(test)
            except queue.Empty:

                pass
            except TypeError :
                pass
            incomming_message = self.__read_incomming_data()

            if incomming_message and incomming_message != 'SensorArduino:0':
#                 print(incomming_message)
                splitted_incomming_message = incomming_message.split(":",1)
                if splitted_incomming_message[0] in self.from_arduino_to_arduino:
                    self.from_arduino_to_arduino_queue.put(incomming_message)
                self.input_queue.put(incomming_message)



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
                    print(output, '    ', str(self.counter), '    ', self.baud_rate)
                    self.counter = self.counter +1
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
#         seperation_char = ':'
#         message_received = ''
        try:
            message_received = self.serial_port.readline()
            message_received = message_received.strip()
            message_received = message_received.decode('utf-8').strip(start_char).strip(end_char)
            return message_received
        except (Exception) as e:
            print(e, 'serial1')
        
    def stop_thread(self):
        self.stop = True
        self.serial_port.close()
        print('closed port', self.serial_port.isOpen())
        
if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()
    ser = SerialWriterReader(q1,q2,'/dev/ttyUSB1', 115200)
    ser.start()
    while True:
        try:
            print(q2.get_nowait())
        except queue.Empty:
            pass