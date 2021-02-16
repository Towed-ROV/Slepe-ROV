from send_and_receive.message_receiver import MessageReceiver
from payloads.payload_reader import PayloadReader
from GPIO_writer import GPIOWriter
from collections import deque
from threading import Thread
class PayloadHandler(Thread):
    def __init__(self, sensor_list, command_queue):
        """
        Handles
        :param sensor_list:
        :param command_queue:
        """
        Thread.__init__(self)
        self.sensor_list = sensor_list
        self.received_data = ""
        self.message_queue = deque()
        self.message_receiver = MessageReceiver(self.message_queue)
        self.message_receiver.daemon = True
        self.message_receiver.start()
        self.command_queue = command_queue
        self.gpio_writer = GPIOWriter()
        self.payload_reader = PayloadReader()

    def run(self):
        while True:
            try:
                self.__sort_payload()
                self.__update_pitch()
            except (Exception) as e:
                print(e, "payload handler")

    def __sort_payload(self):
        """
        takes the received payload and reads it and either handles it or forwards it to the serial output queue
        """
        try:
            payload_type, payload_name, payload_data = self.payload_reader.read_payload(self.message_queue.popleft())
            if payload_type == 'commands':
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
                self.gpio_writer.adjust_camera(sensor[1].strip())



if __name__ == "__main__":
    sensor_list = []
    sensor_list.append("fuck : 8")
    queue = deque()
    payload = PayloadHandler(sensor_list, queue)
    payload.update_pitch()



