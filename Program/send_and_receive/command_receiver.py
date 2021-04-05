from threading import Thread
import zmq


class CommandReceiver(Thread):
    """ DOCS """

<<<<<<< HEAD
    def __init__(self, cmd_queue, host="192.168.0.20", port=8766):
=======
    def __init__(self, cmd_queue, host="192.168.0.223", port=8766):
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        Thread.__init__(self)
        self.ctx = zmq.Context()
        self.connection = self.ctx.socket(zmq.REP)
        self.cmd_queue = cmd_queue
        self.host = host
        self.port = port

    def bind(self):
<<<<<<< HEAD
        self.connection.bind("tcp://10.0.0.54:8767")
=======
        self.connection.bind("tcp://192.168.0.102:8764")
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
        print("[STARTED] CommandReceiver")
        

    def send(self, data):
        self.connection.send_json(data)

    def recv(self):
        test =  self.connection.recv_json()
        print(test)
        return test

    def run(self):
        self.bind()
        while True:
            try:
                cmd = self.recv()
<<<<<<< HEAD
                self.cmd_queue.put(cmd)
                self.send({"succese" : True})
            except (Exception) as e:
                print(e, 'command_receiver')
=======
                self.cmd_queue.append(cmd)
                self.send({"succese" : True})
            except (Exception) as e:
                pass
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
