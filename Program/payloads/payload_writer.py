import json
import time
from send_and_receive.message_dispatcher import MessageDispatcher
from threading import Thread
import queue
from multiprocessing import Queue
class PayloadWriter(Thread):
    def __init__(self, sensor_list, gui_command_queue):
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.message_queue = Queue()
        self.gui_command_queue = gui_command_queue
        self.message_dispatcher = MessageDispatcher(self.message_queue)
        self.message_dispatcher.daemon = True
        self.message_dispatcher.start()
        self.interval = 0.1

    def run(self):
        previousMillis = 0
        while True:
            self.__add_commands_to_queue()
            currentMillis  = time.monotonic()
            if currentMillis - previousMillis >= self.interval:
                self.__merge_sensor_payload()
                previousMillis = currentMillis


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
            time.sleep(0.001)
            sensor_structure = {
                "payload_name": "sensor_data",
                "payload_data": sensors
            }
            
#             print('-----------')
#             print(sensor_structure)
#             print('-----------')

            self.message_queue.put(sensor_structure)

    def __add_commands_to_queue(self):
        try:
            message = self.gui_command_queue.get_nowait()
            print(message)
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
            self.message_queue.put(command_structure)
            print(command_structure)
        except queue.Empty:
            pass
        except IndexError:
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