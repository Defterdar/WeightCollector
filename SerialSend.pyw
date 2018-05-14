import serial
import time

#Seriel
ser = serial.Serial(
    port ='COM4',\
	baudrate=1200,\
    parity=serial.PARITY_EVEN,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.SEVENBITS,\
        timeout=0)

while True:
    for line in open('test.txt'):
        ser.write(line.encode()) 
        print(line)
    time.sleep(0.3)
