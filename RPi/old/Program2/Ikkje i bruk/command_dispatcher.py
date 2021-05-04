from threading import Thread
import zmq


class CommandDispatcher(Thread):
    """ DOCS """

    def __init__(self, cmd_queue, host="127.0.0.1", port=1337):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REQ)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def connect(self):
        self.connection.connect(f"tcp://{self.host}:{self.port}")
        print("[STARTED] CommandDispatcher")

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        return self.connection.recv_json()

    def run(self):
        self.connect()
        while True:
            try:
                cmd = self.cmd_queue.get()
                print("[SENT] ", cmd)
                self.send(cmd)
                response = self.recv()
                print(" [GOT] ", response)
            except KeyboardInterrupt:
                pass
