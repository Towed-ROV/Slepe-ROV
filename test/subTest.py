import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.0.102:8765")
socket.subscribe("")
while True:
    recived_data = json.loads(socket.recv_json())
    print(recived_data)