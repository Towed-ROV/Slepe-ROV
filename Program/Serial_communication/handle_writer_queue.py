class HandleWriterQueue:
    def __init__(self, reader_queue, writer_queue, writer_queue_IMU,
                 writer_queue_sensor_arduino, writer_queue_stepper_arduino):
        self.reader_queue= reader_queue
        self.writer_queue = writer_queue
        self.writer_queue_IMU = writer_queue_IMU
        self.writer_queue_sensor_arduino = writer_queue_sensor_arduino
        self.writer_queue_stepper_arduino = writer_queue_stepper_arduino

    def put_in_writer_queue(self):
        """
        sort message from serial writer queue to the specific writer queue.
        :return: a bool if com port need to be search after.
        """
#todo fiks opp her, dict
        try:
            pitch = self.reader_queue.popleft()
            self.reader_queue.appendleft(pitch)
            for check_pitch in pitch:
                check_pitch = check_pitch.split(':')
                if check_pitch[0] == "pitch":
                    self.__append_stepper_arduino_writer_queue(pitch)
            message = self.writer_queue.popleft()
            item = message.split(':',1)
            if item[0] == 'com_port_search':
                return False
            if item[0] == "reset":
                self.__append_sensor_arduino_writer_queue(message)
                print("append")
            if item[0] == "target_distance":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_depth_p":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_depth_i":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_depth_d":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_trim_p":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_trim_i":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_trim_d":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_seafloor_p":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_seafloor_i":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "pid_seafloor_d":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "emergency_surface":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "target_mode":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "depth_beneath_rov_offset":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "rov_depth_offset":
                self.__append_stepper_arduino_writer_queue(message)
            if item[0] == "arduino sensor":
                self.__append_sensor_arduino_writer_queue(message)
            if item[0] == "arduino stepper":
                self.__append_stepper_arduino_writer_queue(message)
        except IndexError:
            pass
        return True
    def __append_imu_writer_queue(self, message):
        self.writer_queue_IMU.append(message)

    def __append_sensor_arduino_writer_queue(self, message):
        self.writer_queue_sensor_arduino.append(message)

    def __append_stepper_arduino_writer_queue(self, message):
        self.writer_queue_stepper_arduino.append(message)
