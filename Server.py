import socket
import threading
import test
class server:
    def __init__(self, port, data):
        self.data = data
        self.port = port
        self.sock = 0
    def run(self):
        self.openServerSocket()

        while ()

        threading.Thread()
    def openServerSocket(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('192.168.0.100', 9006))
        self.serverSocket.listen(1)
        while True:
            connection, clientAddress = self.serverSocket.accept()
