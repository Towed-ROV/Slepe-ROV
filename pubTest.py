import zmq
import json
import time
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:1337")


data_to_publish = {
    "payload_name": "sensor_data",
    "payload_data": [
        {
            "sensor_name": "pressure_sensor",
            "sensor_value": [
                {
                    "pressure": 111,
                    "depth": 222,
                    "temperature": 333
                }
            ]
        },
        {
            "sensor_name": "IMU",
            "sensor_value": [
                {
                    "heading": 444,
                    "pitch": 555,
                    "roll": 666
                }
            ]
        },
        {
            "sensor_name": "test",
            "sensor_value": 23
        }

    ]
}


while True:
    time.sleep(5)
    socket.send_json(json.dumps(data_to_publish))




