import json
import zmq
from threading import Thread


class MessageReceiver(Thread):
    """ZMQ subscriber running in a seperate thread to poll data from the onshore RPi in suitcase.

    SUB / PUB is connectionless, so it doesnt care if you disconnect, it will
    continously try to re-read from the socket. So any disconnect / reloads or similar doesnt matter,
    because the subscriber will always listen for reconnects
    """
    def __init__(self, queue):
        Thread.__init__(self)
        self.ip = 'tcp://192.168.0.110:8765'
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(self.ip)
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









