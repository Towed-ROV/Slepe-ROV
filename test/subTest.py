import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.0.0.54:8765")
socket.subscribe("")
while True:
    try:
<<<<<<< HEAD
        recived_data = json.loads(socket.recv_json())
        print(recived_data)
    except(Exception) as e:
        print(e)
=======
        received_data = json.loads(socket.recv_json())
        data = received_data['payload_name']
        data = data.split(':',1)
        print(received_data)
        if data[0] ==  'commands':
            print(received_data['payload_data'])
            break
    except (Exception) as e:
        pass
>>>>>>> 1284c7d5cf3e1ec050b021075f895b6fdd3de53d
