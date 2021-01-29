import zmq
import json

class MessageDispatcher:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://192.168.0.20:1337")

    def publish(self, data_to_publish):
        self.socket.send_json(json.dumps(data_to_publish))




