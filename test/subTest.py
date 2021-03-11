import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.0.102:8765")
socket.subscribe("")
while True:
    try:
        received_data = json.loads(socket.recv_json())
        data = received_data['payload_name']
        data = data.split(':',1)
        print(received_data)
        if data[0] ==  'commands':
            print(received_data['payload_data'])
            break
    except (Exception) as e:
        pass