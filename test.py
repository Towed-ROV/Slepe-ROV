import io
class WorkerRunnable:
    def __init__(self, data, clientSocket):
        self.data = data
        self.sepChar = ":"
        self.clientSocket = clientSocket
        self.bufferSize = 1024

    def run(self):
        clientOnline = True
        try:
            recvMessage = self.clientSocket.recv(self.bufferSize)
            recvMessage = str(recvMessage, 'utf-8').rstrip("\r\n")
            if recvMessage:
                recvMessage = recvMessage.split(self.sepChar)
                cmd = recvMessage[0]
                value = recvMessage[1]
                if cmd:
            else:
                print("no data recived")
        except (Exception) as e:
            print(e)

