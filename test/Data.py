class data:
    def __init__(self, publisher):
        self.comPortList = {}
        self.publisher = publisher
        # Sensor data
        self.pitch = 0
        self.roll = 0
        self.heading = 0

        self.wing_pos_port = 0
        self.wing_pos_sb = 0

        self.depth_beneath_rov = 0
        self.rov_depth = 0
        self.rov_pressure = 0

        self.temperature = 0

        # Commands
        self.ack = 0
        self.reset = 0

        self.lights_on_off = 0

        self.pid_depth_p = 0
        self.pid_depth_i = 0
        self.pid_depth_d = 0
        self.pid_trim_p = 0
        self.pid_trim_i = 0
        self.pid_trim_d = 0

        self.

    def set_roll(self, roll):
        self.roll = roll

    def get_roll(self):
        return self.roll

    def set_pitch(self, pitch):
        self.pitch = pitch

    def get_pitch(self):
        return self.pitch

    def set_heading(self, heading):
        self.heading = heading

    def get_heading(self):
        return self.heading

    def set_confirmation(self, ack):
        if self.ack != ack:
            self.publisher.publish(ack)
            self.ack = False ##hei j;rgen fiks det her, loop

    def set_reset(self, reset):
        self.reset = reset
        ##send til serial

    def getAllSensorData(self):
        data = {
            "payload_name": "sensor_data",
            "payload_data": [
                {
                    "sensor_name": "pressure_sensor",
                    "sensor_value": [
                        {
                            "pressure": self.rov_pressure,
                            "depth": self.rov_depth,
                            "temperature": self.temperature
                        }
                    ]
                },
                {
                    "sensor_name": "IMU",
                    "sensor_value": [
                        {
                            "heading": self.heading,
                            "pitch": self.pitch,
                            "roll": self.roll
                        }
                    ]
                },
                {
                    "sensor_name" : "stepperMotor",
                    "sensor_value" : [
                        {
                            "wing_pos_port" : self.wing_pos_port,
                            "wing_pos_sb" : self.wing_pos_sb
                        }
                    ]
                    "sensor_name" : ""
                }
            ]
        }