class Sensor:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_sensor_value(self, value):
        self.value = value

    def get_sensor_value(self):
        return self.value