from send_and_receive.message_receiver import MessageReceiver
<<<<<<< Updated upstream
from payloads.payload_reader import PayloadReader
from GPIO_writer import GPIOWriter
=======
from send_and_receive.command_receiver import CommandReceiver
from payloads.payload_reader import PayloadReader
# from Program.GPIO_writer import GPIOWriter
>>>>>>> Stashed changes
from collections import deque
import json
from threading import Thread


class PayloadHandler(Thread):
<<<<<<< Updated upstream
    def __init__(self, sensor_list, command_queue, start):
=======
    def __init__(self, sensor_list, command_queue):
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        self.gpio_writer = GPIOWriter()
        self.payload_reader = PayloadReader()
        self.start = start
=======
        # self.gpio_writer = GPIOWriter()
        self.payload_reader = PayloadReader()
        self.start_rov = 1
        self.commands_to_serial = {'com_port_search', 'reset', 'com_port_search',
                                   'pid_depth_p', 'pid_depth_i', 'pid_depth_d', 'pid_roll_p',
                                   'pid_roll_i', 'pid_roll_d', 'manual_wing_pos_up', 'manual_wing_pos_down',
                                   'emergency_surface', 'depth_beneath_rov_offset', 'depth_rov_offset'}
        self.commands_to_handle = {'lights_on_off', 'camera_offset_angle', 'start_system', 'depth_or_seafloor'}
>>>>>>> Stashed changes

    def run(self):
        while True:
            try:
<<<<<<< Updated upstream
                self.__sort_payload()
                self.__update_pitch()
=======
                self.__update_pitch()
                self.__sort_payload()
>>>>>>> Stashed changes
            except (Exception) as e:
                print(e, 'payload handler')

    def __sort_payload(self):
        """
        takes the received payload and reads it and either handles it or forwards it to the serial output queue
        """
        try:
<<<<<<< Updated upstream
            payload_type, payload_name, payload_data = self.payload_reader.read_payload(self.message_queue.popleft())
            if payload_type == 'commands':
                if payload_name == 'start':
                    self.start = 1
                if payload_name == 'stop':
                    self.start = 2
                if payload_name == 'reset':
                    self.command_queue.append("reset:" + payload_data)
                if payload_name == 'light_on_off':
                    self.gpio_writer.set_lights(payload_data)
                if payload_name == 'manual_camera_tilt_offset':
                    self.gpio_writer.set_manual_offset_camera_tilt(payload_data)
                if payload_name == 'target_distance':
                    self.command_queue.append("target_distance:" + payload_data)
                if payload_name == 'pid_depth_p':
                    self.command_queue.append("pid_depth_p:" + payload_data)
                if payload_name == 'pid_depth_i':
                    self.command_queue.append("pid_depth_i:" + payload_data)
                if payload_name == 'pid_depth_d':
                    self.command_queue.append("pid_depth_d:" + payload_data)
                if payload_name == 'pid_trim_p':
                    self.command_queue.append("pid_trim_p:" + payload_data)
                if payload_name == 'pid_trim_i':
                    self.command_queue.append("pid_trim_i:" + payload_data)
                if payload_name == 'pid_trim_d':
                    self.command_queue.append("pid_trim_d:" + payload_data)
                if payload_name == 'emergency_surface':
                    self.command_queue.append("emergency_surface:" + payload_data)
                if payload_name == 'target_mode':
                    self.command_queue.append("target_mode:" + payload_data)
                if payload_name == 'com_port_search':
                    self.command_queue.append("com_port_search:" + payload_data)
                if payload_name == 'camera_zero_point':
                    self.command_queue.append("camera_zero_point:" + payload_data)
                if payload_name == 'depth_beneath_rov_offset':
                    self.command_queue.append("depth_beneath_rov_offset:" + payload_data)
                if payload_name == 'rov_depth_offset':
                    self.command_queue.append("rov_depth_offset:" + payload_data)
            if payload_type == '':
                if payload_name == 'arduino sensor':
                    self.command_queue("arduino sensor:" + payload_data)
                if payload_name == 'arduino stepper':
                    self.command_queue("arduino stepper:" +  payload_data)
=======
            payload_type, payload_names, payload_data = self.payload_reader.read_payload(self.message_queue.popleft())
            print(payload_type)
            print(payload_names)
            print(payload_data)
            if payload_type == 'commands':
                if payload_data[0] in self.commands_to_serial:
                    self.command_queue.append(payload_data[0] + ':' + payload_data[1])
                elif payload_data[0] == 'start_system':
                    self.start_rov = payload_data[1]
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

>>>>>>> Stashed changes
        except (IndexError) as e:
            pass

    def __update_pitch(self):
        """
        reads the value of the pitch sensor and send this to the camera servo,
        so it can adjust its angle according to pitch
        """
        for sensor in self.sensor_list:
            sensor = sensor.split(':', 1)
            if sensor[0].strip() == 'pitch':
                # self.gpio_writer.adjust_camera(sensor[1].strip())
                pass


<<<<<<< Updated upstream

if __name__ == "__main__":
=======
if __name__ == '__main__':
>>>>>>> Stashed changes
    sensor_list = []
    start1 = False
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
                    "test": 123
                }
            ]
        }
    )
    ))
    payload.run()
