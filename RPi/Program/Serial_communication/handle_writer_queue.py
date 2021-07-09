import queue


class HandleWriterQueue:
    def __init__(self, reader_queue, writer_queue, writer_queue_IMU,
                 writer_queue_sensor_arduino, writer_queue_stepper_arduino, from_arduino_to_arduino_queue, VALID_SENSOR_LIST):
        self.reader_queue= reader_queue
        self.writer_queue = writer_queue
        self.writer_queue_IMU = writer_queue_IMU
        self.writer_queue_sensor_arduino = writer_queue_sensor_arduino
        self.writer_queue_stepper_arduino = writer_queue_stepper_arduino
        self.from_arduino_to_arduino_queue = from_arduino_to_arduino_queue
        self.VALID_SENSOR_LIST = VALID_SENSOR_LIST

        self.arduino_stepper_commands = ['arduino_stepper', 'auto_mode', 'reset', 'set_point_depth',
                               'pid_depth_p', 'pid_depth_i', 'pid_depth_d', 'pid_roll_p',
                               'pid_roll_i', 'pid_roll_d', 'manual_wing_pos',
                               'emergency_surface', 'depth', 'roll']
        self.arduino_sensor_commands = ['arduino_sensor', 'depth_beneath_rov_offset', 'depth_rov_offset']

    def put_in_writer_queue(self):
        """
        sort message from serial writer queue to the specific writer queue.
        :return: a bool if com port need to be search after.
        """

        try:

            from_arduino_to_arduino = self.from_arduino_to_arduino_queue.get(timeout=0.005)
#             print(from_arduino_to_arduino)
            self.reader_queue.put(from_arduino_to_arduino)
            sensor = from_arduino_to_arduino.split(':')
            if sensor[0] == 'roll':
                self.__append_stepper_arduino_writer_queue(from_arduino_to_arduino)
            elif sensor[0] == 'depth':
                self.__append_stepper_arduino_writer_queue(from_arduino_to_arduino)
            elif sensor[0] == 'pitch':
                self.__append_stepper_arduino_writer_queue(from_arduino_to_arduino)
        except queue.Empty:
            pass
        try:
            message = self.writer_queue.get(timeout=0.005)
            item = message.split(':',1)
            if item[0] == 'arduino_sensor':
                sensor = item[1].split(':',1)
                self.VALID_SENSOR_LIST.append(sensor[1])
                self.__append_sensor_arduino_writer_queue(item[1])
            elif item[0] == 'arduino_stepper':
                stepper = item[1].split(':',1)
                self.VALID_SENSOR_LIST.append(sensor[1])
                self.__append_sensor_arduino_writer_queue(item[1])
            elif item[0] in self.arduino_sensor_commands:
                self.__append_sensor_arduino_writer_queue(message)
            elif item[0] in self.arduino_stepper_commands:
                print("handlewriter" , message)
                self.__append_stepper_arduino_writer_queue(message)
            elif item[0] == 'com_port_search':
                return False
            else:
                print("no command!")
        except queue.Empty:
            pass
        return True

    def __append_imu_writer_queue(self, message):
        self.writer_queue_IMU.put(message)

    def __append_sensor_arduino_writer_queue(self, message):
        self.writer_queue_sensor_arduino.put(message)

    def __append_stepper_arduino_writer_queue(self, message):
        self.writer_queue_stepper_arduino.put(message)
