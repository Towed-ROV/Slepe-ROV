import cameraStream
import threading
import Data
import SerialHandler
import SerialReader
import MessageDispatcher
import Subscriber
class Main:
    def __init__(self):
        self.udpIp = '192.168.0.120'
        self.udpPort = 8083

        self.data = Data.data()
    def run(self):
        self.serial_data_handler = SerialHandler.SerialDataHandler
        self.thread_com_ports(self.serial_data_handler)
        cam = cameraStream.UdpClient(self.udpIp, self.udpPort, self.data)
        t1 = threading.Thread(cam.videoStream())
        t1.daemon = True
        t1.start()
        self.publisher = MessageDispatcher.Publisher()
        sensor_data_thread = threading.Thread(self.send_sensor_data())
        sensor_data_thread.daemon = True
        sensor_data_thread.start()
    def thread_com_ports(self, serialDataHandler):

        for key, value in self.serial_data_handler.port_name_list.items():
            if "IMU" in value:

                imuThread = threading.Thread(SerialReader.ReadSerialData(self.data, 1, 9200, 'imu').run())
                imuThread.start()
            if "stepperArduino" in value>
                stepperReadThread = threading.Thread(SerialReader.ReadSerialData(self.data, 1, 9200, 'imu').run())
                stepperReadThread.start()

    def send_sensor_data(self):
        self.publisher.publish(self.data.getAllSensorData())

class payload_writer:
