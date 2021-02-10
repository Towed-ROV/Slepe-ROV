import zmq
import json
import time
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://192.168.0.20:8765")


data_to_publish = {
    "payload_name": "commands",
    "payload_data": [
        {
            "pressure" : "10"
        }

    ]
}


while True:
    time.sleep(1)
    socket.send_json(json.dumps(data_to_publish))
    print("publish")



