from message_receiver import MessageReceiver
from collections import deque
class PayloadHandler:
    def __init__(self, store_data, command_list):
        self.store_data = store_data
        self.command_list = command_list
        self.received_data = ""
        self.message_queue = deque()
        self.message_receiver = MessageReceiver(self.message_queue)

    def run(self):
        while True:
            try:
                self.__payload_handler()
            except (Exception) as e:
                print(e)

    def __payload_handler(self):
        data_type, data = self.__payload_reader(self.message_queue.popleft())
        if data_type == 'commands':
            for commands in data:
                command_name = commands['command_name']
                command_data = commands['command_value']
                if command_name == 'reset':
                    self.store_data.set_reset(command_data['reset'])
                if command_name == 'light on off':
                    self.store_data.set_light(command_data['light on off'])
                if command_name == 'target distance':
                    self.store_data.set_target_distance(command_data['target distance'])
                if command_name == 'pid parameter depth':
                    command_data = commands['command_value'][0]
                    self.store_data.set_pid_depth_p(command_data['p'])
                    self.store_data.set_pid_depth_i(command_data['i'])
                    self.store_data.set_pid_depth_d(command_data['d'])
                if command_name == 'pid parameter trim':
                    command_data = commands['command_value'][0]
                    self.store_data.set_pid_trim_p(command_data['p'])
                    self.store_data.set_pid_trim_i(command_data['i'])
                    self.store_data.set_pid_trim_d(command_data['d'])
                if command_name == 'emergency surface':
                    self.store_data.set_emergency_surface(command_data['emergency surface'])
                if command_name == 'target mode':
                    self.store_data.set_target_mode(command_data['target mode'])
                if command_name == 'com port search':
                    self.store_data.set_com_port_search(command_data['com port search'])
                if command_name == 'camera zero point':
                    self.store_data.set_camera_zero_point(command_data['camera zero point'])
                if command_name == 'depth beneath rov offset':
                    self.store_data.set_depth_beneath_rov_offset(command_data['depth beneath rov offset'])
                if command_name == 'rov depth offset':
                    self.store_data.set_rov_depth_offset(command_data['rov depth offset'])
        if data_type == 'sensor_data':
            pass
        self.received_data = ""
    def __payload_reader(self, received_data):
        data_type = received_data['payload_name']
        data = received_data['payload_data']
        return data_type, data
    def set_command_list(self, command_list):
        self.command_list = command_list
    def set_received_data(self, received_data):
        self.received_data = received_data