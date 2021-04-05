import json
import zmq
from threading import Thread
class MessageReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
<<<<<<< HEAD
        self.ip = 'tcp://10.0.0.54:8764'
=======
        self.ip = 'tcp://192.168.0.20:8765'
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.ip)
        self.socket.subscribe('')
        self.queue = queue
        
    def run(self):
        while True:
            try:
                self.subscribe()
            except zmq.ZMQError:
                print('could not receive data')
            except (Exception)as e:
                print(e, 'sada')

    def subscribe(self):
        """
        read data and append to queue
        """
        received_data = self.socket.recv_json()
<<<<<<< HEAD
        self.queue.put(received_data)
=======
        self.queue.append(received_data)
        test = self.queue.popleft()
        self.queue.append(test)
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d

    def connect(self):
        self.socket.connect(self.ip)

    def disconnect(self):
        self.socket.disconnect()









