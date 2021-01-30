import serial


class Arduino():
    """
    Models an Arduino connection
    """

    def __init__(self, PORT='COM3', BAUD_RATE=9600):
        """ Initializes the serial connection settings """
        self.PORT = PORT
        self.BAUD_RATE = BAUD_RATE
        self.is_connected = False
        self.name = "Unknown"

    def connect(self):
        """ Initializes the serial connection to the Arduino board """
        self.connection = serial.Serial(
            port=self.PORT, baudrate=self.BAUD_RATE, timeout=1)
        self.name = self.connection.name
        self.is_connected = True

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def is_connected(self):
        return self.is_connected

    def read_data(self):
        data = self.connection.readline().decode('utf-8')
        self.connection.flushInput()
        return data

    def send_data(self, data):
        stuff = data.encode('utf-8')
        self.connection.write(stuff)


if __name__ == "__main__":

    USB_PORT_LINUX = '/dev/ttyUSB0'
    USB_PORT_WINDOWS = 'COM8'
    BAUD_RATE = 9600

    ino = Arduino(PORT=USB_PORT_WINDOWS, BAUD_RATE=BAUD_RATE)
    ino.connect()

    stuffs = ["hei", "hei", "hei", "hei", "hei"]

    for stuff in stuffs:

        ino.send_data(stuff + "\n")
        response = ino.read_data()

        print("Sent: ", stuff)
        print(" Got: ", response)