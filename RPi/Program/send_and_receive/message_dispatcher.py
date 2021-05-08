import zmq
import queue
from time import time


class MessageDispatcher():
    """
    ZMQ publisher for sending sensor data and responces to commands back to the onshore laptop
    """
    def __init__(self, data_queue):
        self.ip = 'tcp://192.168.0.102:8765'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue
        self.counter = 0

    def publish(self):
        try:
            self.socket.send_json(self.data_queue.get(timeout=0.01))
        except queue.Empty:
            self.counter_skip += 1
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)


