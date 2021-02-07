class Sensor:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def set_sensor_value(self, value):
        self.value = value

    def get_sensor_value(self):
        return self.value