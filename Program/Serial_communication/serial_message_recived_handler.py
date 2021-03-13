from sensor import Sensor
class SerialMessageRecivedHandler:
    def __init__(self, gui_command_queue, sensor_list, valid_sensor_list):
        self.message_received_queue = gui_command_queue
        self.sensor_list = sensor_list
        self.valid_sensor_list = valid_sensor_list
        self.valid_commands = ['reset', 'IMU', 'SensorArduino', 'StepperArduino']


    def handle_message_recevied(self, received_message):
        message = received_message.split(':',1)
        if message[0] in  self.valid_commands:
            self.message_received_queue.append(received_message)
        else:
            self.__add_sensor(message)

    def __add_sensor(self, message):
        """
        checks of message is an expected on, and if, it adds the message/sensor to the list of sensors.
        If the sensor is already in the list it updates it's value.
        :param message:
        """
        if ('IMU' or 'sensorArduino' or 'stepperArduino') in message[0]:
            pass
        else:
            if message[0] in self.valid_sensor_list:
                if message[0] in self.sensor_list.keys():
                    self.sensor_list[message[0]] = message[1]
                else:
                    sensor = Sensor(message[0], message[1])
                    # print('------')
                    # print(sensor)
                    # print('------')
                    self.sensor_list[message[0]] = sensor
