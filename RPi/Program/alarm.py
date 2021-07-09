class Alarm:
    """
    Reprecent sensor object storing the name and the value of a sensor
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_alarm_value(self, value):
        self.value = value

    def get_alarm_value(self):
        return self.value

    def set_alarm_name(self, name):
        self.name = name

    def get_alarm_name(self):
        return self.name