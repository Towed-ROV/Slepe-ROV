from threading import Thread
import zmq


class CommandReceiver(Thread):
    """ DOCS """

    def __init__(self, cmd_queue, host="127.0.0.1", port=1337):
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REP)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def bind(self):
        self.connection.bind(f"tcp://{self.host}:{self.port}")
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
                print(" [GOT] ", cmd)
                self.cmd_queue.put(cmd)
                _response = {"msg": "ok bro"}
                self.send(_response)
                print("[SENT] ", _response)
            except KeyboardInterrupt:
                break
