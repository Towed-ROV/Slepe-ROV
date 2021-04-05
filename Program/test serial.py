import serial

ser = serial.Serial(
    port='/dev/ttyUSB1',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
print("connected to: " + ser.portstr)

#this will store the line
seq = []
count = 1

while True:
    string = ser.readline()
    if string:
        string = string.strip()
        string = string.decode('utf-8').strip('<').strip('>')
        print("Line " + str(count) + ': ' + str(string))

        count += 1


ser.close()