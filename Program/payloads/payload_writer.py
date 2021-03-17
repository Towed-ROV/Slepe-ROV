import json
import time
from send_and_receive.message_dispatcher import MessageDispatcher
from threading import Thread
from collections import deque
class PayloadWriter(Thread):
    def __init__(self, sensor_list, gui_command_queue):
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.message_queue = deque()
        self.gui_command_queue = gui_command_queue
        self.message_dispatcher = MessageDispatcher(self.message_queue)
        self.message_dispatcher.daemon = True
        self.message_dispatcher.start()

    def run(self):
        time.sleep(10)
        while True:
            try:
                self.__add_commands_to_queue()
                self.__merge_sensor_payload()
            except (Exception) as e:
                pass

    def __merge_sensor_payload(self):
        """
        Takes all sensor and creates a json with sensordata, adds the json to a queue.
        """
        sensors = []

        json_sensor = ''
        if self.sensor_list.items():
            for sensor_name, sensor_value in self.sensor_list.items():
                # 
                # sensors.append('%s:%s'%sensor_name, sensor_value)
            
                sensors.append({"name" : sensor_name,
                                "value" : sensor_value})
#                 print(type(sensor_value))   
    #         for sensor_name, sensor_value in self.sensor_list.items():
                
#     #             sensors.append('%s:%s'%sensor_name, sensor_value)
#             json_sensor = json.dumps(sensors)
            time.sleep(0.05)
            sensor_structure = {
                "payload_name": "sensor_data",
                "payload_data": sensors
            }
            
    #         print('-----------')
    #         print(sensor_structure)
    #         print('-----------')

            self.message_queue.append(sensor_structure)

    def __add_commands_to_queue(self):
        try:
            message = self.gui_command_queue.popleft()
            message = message.split(":",1)
            if message[1] == "True":
                message[1] = True
            elif message[1] == "False":
                message[1] = False
            json_command = [{"name" : message[0],
                        "success" : message[1]}]
            command_structure = {
                "payload_name": "response",
                "payload_data": json_command
            }
            self.message_queue.appendleft(command_structure)
            print("appended")
        except (Exception) as e:
            pass

if __name__ == '__main__':
    sensor_list = {}
    sensor_list["test"] = 10
    sensor_list["test2"] = 123
    sensor_list["kr[re"] = 1231231
    payload = PayloadWriter()
    test = payload.merge_payload(sensor_list)

response_structure = {
                "payload_name": "response",
                "payload_data": [
                    {
                        "command": "manual_wing_pos_up",
                        "success": True
                    }
                ]
            }