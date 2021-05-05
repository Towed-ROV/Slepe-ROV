import json
import zmq
from threading import Thread


class MessageReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.ip_boat = 'tcp://127.0.0.1:6969'
        self.ip_api = 'tcp://127.0.0.1:42069'
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.ip_boat)
        self.socket.connect(self.ip_api)
        self.socket.subscribe('')
        self.queue = queue

    def run(self):
        while True:
            try:
                self.recv()
            except zmq.ZMQError:
                print('could not receive data')
            except (Exception)as e:
                print(e, 'sada')

    def recv(self):
        """
        read data and append to queue
        """
        received_data = self.socket.recv_json()
        self.queue.put(received_data)

    def connect(self):
        self.socket.connect(self.ip)

    def disconnect(self):
        self.socket.disconnect()
