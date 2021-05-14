import zmq
import queue
from time import time


class MessageDispatcher():
    def __init__(self, data_queue):
        self.ip = 'tcp://127.0.0.1:13372'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.data_queue = data_queue
        self.counter = 0

        self.counter_sent = 0
        self.counter_skip = 0
        tim = time()
        self.start = tim

    def publish(self):
        try:
            test = self.data_queue.get(timeout=0.01)
            self.counter_sent += 1
            # print("send",test)
            self.socket.send_json(test)
            # self.counter = self.counter +1
            # print(self.counter)
        except queue.Empty:
            self.counter_skip += 1
        # DEBUGG HELP

    #         if (time() - self.start) > 5:
    #             print("TIME________: ", str(time() - self.start))
    #             print("Times sent  : ", str(self.counter_sent))
    #             print("Times skips : ", str(self.counter_skip))
    #             self.counter_sent = 0
    #             self.counter_skip = 0
    #             self.start = time()

    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)
