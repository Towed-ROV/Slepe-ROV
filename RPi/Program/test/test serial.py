import serial

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=57600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
print("connected to: " + ser.portstr)

#this will store the line
seq = []
count = 1

while True:
    string = ser.read(8)
    if string:
        print(string) 


ser.close()