from Program.send_and_receive.message_receiver import MessageReceiver
from Program.send_and_receive.command_receiver import CommandReceiver
from Program.payloads.payload_reader import PayloadReader
# from Program.GPIO_writer import GPIOWriter
from collections import deque
import json
from threading import Thread
class PayloadHandler(Thread):
    def __init__(self, sensor_list, command_queue, start1):
        """
        Handles
        :param sensor_list:
        :param command_queue:
        """
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.received_data = ''
        self.message_queue = deque()
        self.message_receiver = MessageReceiver(self.message_queue)
        self.message_receiver.daemon = True
        self.message_receiver.start()
        self.command_receiver = CommandReceiver(self.message_queue)
        self.command_receiver.daemon = True
        self.command_receiver.start()
        self.command_queue = command_queue
        # self.gpio_writer = GPIOWriter()
        self.payload_reader = PayloadReader()
        self.start1 = True
        self.commands_to_serial = {'com_port_search', 'reset', 'com_port_search',
                               'pid_depth_p', 'pid_depth_i', 'pid_depth_d', 'pid_roll_p',
                               'pid_roll_i', 'pid_roll_d', 'manual_wing_pos_up', 'manual_wing_pos_down',
                               'emergency_surface', 'depth_beneath_rov_offset', 'depth_rov_offset' }
        self.commands_to_handel = {'lights_on_off', 'camera_offset_angle', 'start_system', 'depth_or_seafloor'}

    def run(self):
        while True:
            try:
                self.__sort_payload()
                self.__update_pitch()
            except (Exception) as e:
                print(e, 'payload handler')

    def __sort_payload(self):
        """
        takes the received payload and reads it and either handles it or forwards it to the serial output queue
        """
        try:
            test = self.message_queue.popleft()
            print(test)
            payload_type, payload_names, payload_data = self.payload_reader.read_payload(test)
            print(payload_type)
            print(payload_names)
            print(payload_data)
            if payload_type == 'commands':
                if payload_data[0] in self.commands_to_serial:
                    self.command_queue.append(payload_data[0] + ':' + payload_data[1])
                elif payload_data[0] == 'start_system':
                    self.start1 = payload_data[1]
                elif payload_data[0] == 'light_on_off':
                    pass
                    # self.gpio_writer.set_lights(payload_data)
                elif payload_data[0] == 'camera_offset_angle':
                    pass
                    # self.gpio_writer.set_manual_offset_camera_tilt(payload_data)
                elif payload_data[0] == 'depth_or_seafloor':
                    self.command_queue.append('depth_or_seafloot:' + payload_data[1])
            if payload_type == 'settings':
                if payload_data[0] == 'arduino sensor':
                    self.command_queue.append('arduino_sensor:' + payload_data[1] + ':' + payload_data[2])
                if payload_data[0] == 'arduino stepper':
                    self.command_queue.append('arduino_stepper:' + payload_data[1] + ':' + payload_data[2])
            # if payload_type == 'request':

        except (IndexError) as e:
            pass
        

    def __update_pitch(self):
        """
        reads the value of the pitch sensor and send this to the camera servo,
        so it can adjust its angle according to pitch
        """
        for sensor in self.sensor_list:
            sensor = sensor.split(':',1)
            if sensor[0].strip() == 'pitch':
                # self.gpio_writer.adjust_camera(sensor[1].strip())
                pass


if __name__ == '__main__':
    sensor_list = []
    start1 =  False
    sensor_list.append('fuck : 8')
    queue = deque()

    payload = PayloadHandler(sensor_list, queue, start1)

    payload.message_queue.append(json.loads(json.dumps(
        {
            "payload_name": "commands",
            "payload_data": [
                {
                    "name": "start",
                    "value": 0.00,
                    "test" : 123
                }
            ]
        }
    )
    ))
    payload.run()