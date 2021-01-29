import json
import zmq

class Subscriber:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://192.168.0.120:1337")

    def subscribe(self, store_data):
        store_data = store_data
        recived_data = json.loads(self.socket.recv_json())
        data_type = recived_data['payload_name']
        data = recived_data['payload_data']
        if data_type == 'commands':
            for commands in data:
                command_name = commands['command_name']
                command_data = commands['command_value']
                if command_name == 'reset':
                    store_data.set_reset(command_data['reset'])
                if command_name == 'light on off':
                    store_data.set_light(command_data['light on off'])
                if command_name == 'target distance':
                    store_data.set_target_distance(command_data['target distance'])
                if command_name == 'pid parameter depth':
                    command_data = commands['command_value'][0]
                    store_data.set_pid_depth_p(command_data['p'])
                    store_data.set_pid_depth_i(command_data['i'])
                    store_data.set_pid_depth_d(command_data['d'])
                if command_name == 'pid parameter trim':
                    command_data = commands['command_value'][0]
                    store_data.set_pid_trim_p(command_data['p'])
                    store_data.set_pid_trim_i(command_data['i'])
                    store_data.set_pid_trim_d(command_data['d'])
                if command_name == 'emergency surface':
                    store_data.set_emergency_surface(command_data['emergency surface'])
                if command_name == 'target mode':
                    store_data.set_target_mode(command_data['target mode'])
                if command_name == 'com port search':
                    store_data.set_com_port_search(command_data['com port search'])
                if command_name == 'camera zero point':
                    store_data.set_camera_zero_point(command_data['camera zero point'])
                if command_name == 'depth beneath rov offset':
                    store_data.set_depth_beneath_rov_offset(command_data['depth beneath rov offset'])
                if command_name == 'rov depth offset':
                    store_data.set_rov_depth_offset(command_data['rov depth offset'])
        if data_type == 'sensor_data':








