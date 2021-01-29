class WorkerRunnable:
    def __init__(self, socket, data):
        self.data = data
        self.socket = socket
