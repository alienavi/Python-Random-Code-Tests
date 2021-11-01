import serial

ser = serial.Serial('COM7')
ser.timeout = 1

def find_br(packet) :
    for br in ser.BAUDRATES :
        ser.baudrate = br
        ser.write(packet)
        print(br, " : ", ser.readline())

find_br(str.encode('AT\r\n'))
find_br(str.encode('AT+BAUD\r\n'))

def sstr(data) :
    return str.encode(data+'\r\n')

ser.baudrate = 2475
ser.write(sstr('AT'))
print(ser.readline())
ser.write(sstr('AT+BAUD'))
print(ser.readline())
ser.write(sstr('AT+NAME'))
print(ser.readline())
ser.write(sstr('AT+BAUD?'))
print(ser.readline())
ser.write(sstr('AT+NAME?'))
print(ser.readline())
ser.write(sstr('AT+VERSION'))
print(ser.readline())
ser.write(sstr('AT+RESET'))
print(ser.readline())
