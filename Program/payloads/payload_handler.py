from send_and_receive.message_receiver import MessageReceiver
from GPIO_writer import GPIOWriter
from collections import deque
from threading import Thread
class PayloadHandler(Thread):
    def __init__(self, sensor_list, command_queue):
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.received_data = ""
        self.message_queue = deque()
        self.message_receiver = MessageReceiver(self.message_queue)
        self.message_receiver.daemon = True
        self.message_receiver.start()
        self.command_queue = command_queue
        self.gpio_writer = GPIOWriter()

    def run(self):
        while True:
            try:
                self.__handle_payload()
                # self.__update_pitch()
            except (Exception) as e:
                print(e, "payload handler")

    def __handle_payload(self):
        """
        takes the received payload and reads it and either handles it or forwards it to the serial output queue
        """
        try:
            data_type, data = self.__payload_reader(self.message_queue.popleft())
            if data_type == 'commands':
                command_name = data.split(':',1)[0].replace('{','').replace('"',"").strip()
                command_data = data.split(':',1)[1].replace('}','').replace('"',"").strip()
                print(command_name)
                print(command_data)
                
                if command_name == 'reset':
                    self.command_queue.append("reset:" + command_data)
                    print('tet')
                if command_name == 'light_on_off':
                    self.gpio_writer.set_lights(command_data)
                if command_name == 'manual_camera_tilt_offset':
                    self.gpio_writer.set_manual_offset_camera_tilt(command_data)
                if command_name == 'target_distance':
                    self.command_queue.append("target_distance:" + command_data)
                if command_name == 'pid_depth_p':
                    self.command_queue.append("pid_depth_p:" + command_data)
                if command_name == 'pid_depth_i':
                    self.command_queue.append("pid_depth_i:" + command_data)
                if command_name == 'pid_depth_d':
                    self.command_queue.append("pid_depth_d:" + command_data)
                if command_name == 'pid_trim_p':
                    self.command_queue.append("pid_trim_p:" + command_data)
                if command_name == 'pid_trim_i':
                    self.command_queue.append("pid_trim_i:" + command_data)
                if command_name == 'pid_trim_d':
                    self.command_queue.append("pid_trim_d:" + command_data)
                if command_name == 'emergency_surface':
                    self.command_queue.append("emergency_surface:" + command_data)
                if command_name == 'target_mode':
                    self.command_queue.append("target_mode:" + command_data)
                if command_name == 'com_port_search':
                    self.command_queue.append("com_port_search:" + command_data)
                if command_name == 'camera_zero_point':
                    self.command_queue.append("camera_zero_point:" + command_data)
                if command_name == 'depth_beneath_rov_offset':
                    self.command_queue.append("depth_beneath_rov_offset:" + command_data)
                if command_name == 'rov_depth_offset':
                    self.command_queue.append("rov_depth_offset:" + command_data)
        except (IndexError) as e:
            pass
        

    def update_pitch(self):
        """
        reads the value of the pitch sensor and send this to the camera servo,
        so it can adjust its angle according to pitch
        """
        for sensor in self.sensor_list:
            sensor = sensor.split(':',1)
            if sensor[0].strip() == 'pitch':
                self.gpio_writer.adjust_camera(sensor[1].strip())

    def __payload_reader(self, received_data):
        """
        extracts data from message received
        :param received_data: data received from zmq
        :return: the data type and the data
        """
        print(received_data['payload_data'])
        data_type = received_data['payload_name']
        data = received_data['payload_data']
        return data_type, data


if __name__ == "__main__":
    sensor_list = []
    sensor_list.append("fuck : 8")
    queue = deque()
    payload = PayloadHandler(sensor_list, queue)
    payload.update_pitch()



