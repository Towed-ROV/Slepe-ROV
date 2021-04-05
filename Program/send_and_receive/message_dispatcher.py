import zmq
import queue
from threading import Thread

class MessageDispatcher(Thread):
    def __init__(self, data_queue):
        Thread.__init__(self)
        self.ip = 'tcp://192.168.0.102:8765'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue
        self.counter = 0

    def run(self):
        while True:
            try:
                self.publish()
            except queue.Empty:
                pass

    def publish(self):
        test = self.data_queue.get_nowait()
#         print('dispatch data')
        self.socket.send_json(test)
#         self.counter = self.counter +1
#         print(self.counter)
        
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)


