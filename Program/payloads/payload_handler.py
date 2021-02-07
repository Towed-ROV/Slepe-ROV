from send_and_receive.message_receiver import MessageReceiver
from collections import deque
from threading import Thread
class PayloadHandler(Thread):
    def __init__(self, command_queue):
        Thread.__init__(self)
        self.received_data = ""
        self.message_queue = deque()
        self.message_receiver = MessageReceiver(self.message_queue)
        self.command_queue = command_queue

    def run(self):
        while True:
            try:
                self.__handle_payload()
            except (Exception) as e:
                print(e, "payload handler")

    def __handle_payload(self):
        try:
            data_type, data = self.__payload_reader(self.message_queue.popleft())
            if data_type == 'commands':
                for commands in data:
                    command_name = commands['command_name']
                    command_data = commands['command_value']
                    if command_name == 'reset':
                        self.command_queue.append("reset:" + command_data['reset'])
                    if command_name == 'light_on_off':
                        self.command_queue.append("light_on_off:" + command_data['light_on_off'])
                    if command_name == 'target_distance':
                        self.command_queue.append("target_distance:" + command_data['target_distance'])
                    if command_name == 'pid_parameter_depth':
                        command_data = commands['command_value'][0]
                        self.command_queue.append("pid_depth_p:" + command_data['pid_depth_p'])
                        self.command_queue.append("pid_depth_i:" + command_data['pid_depth_i'])
                        self.command_queue.append("pid_depth_d:" + command_data['pid_depth_d'])
                    if command_name == 'pid_parameter_trim':
                        command_data = commands['command_value'][0]
                        self.command_queue.append("pid_trim_p:" + command_data['pid_trim_p'])
                        self.command_queue.append("pid_trim_i:" + command_data['pid_trim_i'])
                        self.command_queue.append("pid_trim_d:" + command_data['pid_trim_d'])
                    if command_name == 'pid_parameter_seafloor':
                        command_data = commands['command_value'][0]
                        self.command_queue.append("pid_seafloor_p:" + command_data['pid_seafloor_p'])
                        self.command_queue.append("pid_seafloor_i:" + command_data['pid_seafloor_i'])
                        self.command_queue.append("pid_seafloor_d:" + command_data['pid_seafloor_d'])
                    if command_name == 'emergency_surface':
                        self.command_queue.append("emergency_surface:" + command_data['emergency_surface'])
                    if command_name == 'target_mode':
                        self.command_queue.append("target_mode:" + command_data['target_mode'])
                    if command_name == 'com_port_search':
                        self.command_queue.append("com_port_search:" + command_data['com_port_search'])
                    if command_name == 'camera_zero_point':
                        self.command_queue.append("camera_zero_point:" + command_data['camera_zero_point'])
                    if command_name == 'depth_beneath_rov_offset':
                        self.command_queue.append("depth_beneath_rov_offset:" + command_data['depth_beneath_rov_offset'])
                    if command_name == 'rov_depth_offset':
                        self.command_queue.append("rov_depth_offset:" + command_data['rov_depth_offset'])
        except (IndexError) as e:
            pass
    def __payload_reader(self, received_data):
        data_type = received_data['payload_name']
        data = received_data['payload_data']
        return data_type, data
    def set_command_list(self, command_list):
        self.command_list = command_list
    def set_received_data(self, received_data):
        self.received_data = received_data