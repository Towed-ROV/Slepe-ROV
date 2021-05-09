import json
import zmq
from threading import Thread


class MessageReceiver(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.ip = 'tcp://localhost:8787'

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.connect(self.ip)
        self.queue = queue

    def run(self):
        while True:
            try:
                print("eyo")
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
        print(received_data)
        self.queue.put(received_data)

    def connect(self,ip):
        self.socket.connect(ip)

    def disconnect(self):
        self.socket.disconnect()
