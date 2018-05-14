import serial
import keyboard
import os
import win32gui
import pyodbc
import socket
import cred

#SQL
cnxn = pyodbc.connect('Trusted_Connection=no',
               driver='{SQL Server}', server=cred.Server,
               uid=cred.User, pwd=cred.Pass, database='weightCollector')
cursor = cnxn.cursor()

#IP
ip = socket.gethostbyname(socket.gethostname())
ip = ip.rsplit('.',2)[1]
cursor.execute('SELECT * FROM [weightCollector].[dbo].[Setup] where ID =('+ip+')')
row = cursor.fetchone()
if row:
    Fabrik = row.Fabrik.strip()

w = win32gui
os.system("mode con cols=40 lines=10")

#Seriel
if 'FA' in str(Fabrik):
    ser = serial.Serial(
        port = input('Enter COM port (Ex. COM1): '),\
        baudrate=1200,\
        parity=serial.PARITY_EVEN,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.SEVENBITS,\
            timeout=0)

if 'KO' in str(Fabrik):
    ser = serial.Serial(
        port = input('Enter COM port (Ex. COM2): '),\
	    baudrate=9600,\
        parity=serial.PARITY_EVEN,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
seq = []
joined_seq = []

while True:
    if 'FA' in str(Fabrik):
        for c in ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq if v in "1234567890 ")
            if chr(c) == '\n':
                print(joined_seq)  
                if "Microsoft Dynamics NAV" in w.GetWindowText (w.GetForegroundWindow()):
                    keyboard.write(joined_seq)
                    keyboard.press_and_release('enter')
                seq = []
                break

    if 'KO' in str(Fabrik):
        raw = ser.readline().decode('utf-8')
        joined_seq = ''.join(str(v) for v in raw if v in "1234567890")
        if len(joined_seq) > 3:
            if joined_seq[0:1] is '0':
                result = int(joined_seq)
                print(result)
                if "Microsoft Dynamics NAV" in w.GetWindowText (w.GetForegroundWindow()):
                    keyboard.write(joined_seq)
                    keyboard.press_and_release('enter')
