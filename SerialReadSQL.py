import serial
import os
import keyboard
import pyodbc
from tkinter import *
import cred

root = Tk()
root.overrideredirect(True)
root.overrideredirect(False)

root.attributes('-fullscreen',False)



os.system("mode con cols=55 lines=10")    

fabrik = input('Indsat fabrikskode (Ex. Fasterholt): ')
#SQL
cnxn = pyodbc.connect('Trusted_Connection=no',
               driver='{SQL Server}', server=cred.Server,
               uid=cred.User, pwd=cred.Pass, database='weightCollector')
cursor = cnxn.cursor()

#Seriel
ser = serial.Serial(
    port = input('Enter COM port (Ex. COM5): '),\
	baudrate=1200,\
    parity=serial.PARITY_EVEN,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.SEVENBITS,\
        timeout=0)

dotTitle = "DOT Vægt   Fabrik: "+fabrik+"   Port: "+ser.portstr
os.system("title "+dotTitle)

print("\033[92mconnected to:\033[93m\033[1m " + ser.portstr)

count = 1
seq = []

#loop
try:
    while True:
        for c in ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq if v in "1234567890 ")

            if chr(c) == '\n':
                sqlTxt = "insert into [weightCollector].[dbo].["+fabrik+"] (value) values ('"+joined_seq.strip()+"')"
                print(joined_seq)
                keyboard.write(joined_seq)
                w = Label(root,text=joined_seq)
                w.pack()
                if count > 200:
                    cursor.execute("delete from [weightCollector].[dbo].["+fabrik+"]")
                    cursor.commit()
                    count = 1
                cursor.execute(sqlTxt)
                cursor.commit()			
                keyboard.press_and_release('tab')
                seq = []
                count += 1 
                break

        root.mainloop()
except KeyboardInterrupt:
    pass

cnxn.close()
ser.close()
