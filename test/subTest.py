import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.0.0.27:8765")
socket.subscribe("")
while True:
    try:
        recived_data = socket.recv_json()
        print(recived_data)
        # if recived_data["payload_name"] == "response":
        #     print(recived_data)
    except(Exception) as e:
        print(e)

