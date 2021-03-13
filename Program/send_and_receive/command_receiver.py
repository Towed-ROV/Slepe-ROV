from threading import Thread
import zmq


class CommandReceiver(Thread):
    """ DOCS """

    def __init__(self, cmd_queue, host="192.168.0.223", port=8766):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REP)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def bind(self):
        self.connection.bind("tcp://192.168.0.102:8764")
        print("[STARTED] CommandReceiver")
        

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.bind()
        while True:
            try:
                cmd = self.recv()
                self.cmd_queue.append(cmd)
                self.send({"succese" : True})
            except (Exception) as e:
                pass