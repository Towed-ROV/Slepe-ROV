import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:1337")
socket.subscribe("")
print("test")
while True:
    recived_data = json.loads(socket.recv_json())
    # print(recived_data)
    data_type = recived_data['payload_name']
    data = recived_data['payload_data']



    for sensor in data:
        sensor_name = sensor['sensor_name']
        if sensor_name == 'pressure_sensor':
            sensor_data = sensor['sensor_value'][0]
            pressure = sensor_data['pressure']
            depth = sensor_data['depth']
            temperature = sensor_data['temperature']
            print(str(pressure) + ':'+str(depth)+':'+str(temperature))
        if sensor_name == 'IMU':
            sensor_data = sensor['sensor_value'][0]
            heading = sensor_data['heading']
            pitch = sensor_data['pitch']
            roll = sensor_data['roll']
            print(str(heading) + ':'+str(pitch)+':'+str(roll))
        if sensor_name == 'test':
            print(sensor['sensor_value'])

