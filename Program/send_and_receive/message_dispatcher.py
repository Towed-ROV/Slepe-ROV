import zmq
<<<<<<< HEAD
import queue
=======
import json
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
from threading import Thread
from time import sleep
class MessageDispatcher(Thread):
    def __init__(self, data_queue):
        Thread.__init__(self)
<<<<<<< HEAD
        self.ip = 'tcp://10.0.0.54:8765'
=======
        self.ip = 'tcp://192.168.0.102:8765'
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue
        self.counter = 0

    def run(self):
        while True:
            try:
                
                self.publish()
<<<<<<< HEAD
            except queue.Empty:
                pass

    def publish(self):
        test = self.data_queue.get_nowait()
#         print('dispatch data')
        self.socket.send_json(test)
#         self.counter = self.counter +1
#         print(self.counter)
=======
                
            except (Exception) as e:
                pass

    def publish(self):
        test = self.data_queue.popleft()
#         print(test, 'dsad')
        self.socket.send_json(test)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)


