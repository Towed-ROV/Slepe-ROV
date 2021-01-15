class data:
    def __init__(self):
        self.comPortList ={}

        #Sensor data
        self.pitch = 0
        self.roll = 0
        self.heading = 0

        self.wingPosPort = 0
        self.wingPosSb = 0

        self.depthBeneathROV = 0
        self.rovDepth = 0
        self.rovPressure = 0

        #Commands
        self.confirmation = 0
        self.reset = 0

        self.lightsOnOff = 0

        self.pidDepthP = 0
        self.pidDepthI = 0
        self.pidDepthD = 0
        self.pidTrimP = 0
        self.pidTrimI = 0
        self.pidTrimD = 0


    def setPitch(self, pitch):
        self.pitch = pitch

    def getPitch(self):
        return self.pitch
