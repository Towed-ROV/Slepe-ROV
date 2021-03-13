import zmq
import json
from threading import Thread
from time import sleep
class MessageDispatcher(Thread):
    def __init__(self, data_queue):
        Thread.__init__(self)
        self.ip = 'tcp://192.168.0.102:8765'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue

    def run(self):
        while True:
            try:
                sleep(0.1)
                
                self.publish()
                
            except (Exception) as e:
                pass

    def publish(self):
        test = self.data_queue.popleft()
        print(test)
        self.socket.send_json(test)
        
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)


