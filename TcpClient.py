import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('192.168.0.102', 9006)
print('Starting up TCP Server')
try:
    sock.bind(serverAddress)
    sock.listen(1)
    while True:
        connection, clientAddress = sock.accept()
        try:
            print('Connection from', clientAddress)

            while True:
                dataRecv = connection.recv(4096)
                dataString = str(dataRecv, 'utf-8').rstrip("\r\n")
                if dataRecv:
                    if dataString == "1":
                        bytesToBeSent = dataToBeSent.encode("UTF-8")
                        connection.sendall(bytesToBeSent)
                    else:
                        print('Wrong command received: ' + dataString)
                        connection.sendall('Wrong command!\r\n')
                else:
                    print('no data from', clientAddress)
                    break

        except (Exception, KeyboardInterrupt) as e:
        connection.close()
        finally:
        connection.close()

except Exception as e:
print("Ip and port not avalible")
