from command_receiver import CommandReceiver
from message_dispatcher import MessageDispatcher
import queue
import time
import random
 
sensor_queue = queue.Queue()
 
sp = MessageDispatcher(sensor_queue)
 
import csv
import pprint
 
fake_payload = {
    "payload_name": "sensor_data",
    "payload_data": []
}
 
payload_names = []
 
f = open("data.csv", newline='')
csv_reader = csv.reader(f)
 
# Add header names
for name in next(csv_reader):
    payload_names.append(name)
 
# INITIAL SHITT 
temp_values = []
for i, value in enumerate(next(csv_reader)):
    temp_values.append(float(value))
# INITIAL SHITT 
temp_sensors = []
for name, value in zip(payload_names, temp_values):
    sensor = {"name": name, "value": value}
    temp_sensors.append(sensor)
 
def get_payload():
    
    # ADD NAMES
    temp_values = []
    for i, value in enumerate(next(csv_reader)):
        temp_values.append(float(value))
    
    # ADD VALUES
    temp_sensors = []
    for name, value in zip(payload_names, temp_values):
        sensor = {"name": name, "value": value}
        temp_sensors.append(sensor)
    
    fake_payload["payload_data"] = temp_sensors
    
    return fake_payload
 
 
 
        
 
while True:
    time.sleep(0.1)
    payload = get_payload()
    sensor_queue.put(payload)
    sp.publish()
 
f.close()
 