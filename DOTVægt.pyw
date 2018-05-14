from tkinter import *
import pyodbc
import serial
import re
import cred

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

root = Tk()
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(3, weight=1)
root.columnconfigure(0, weight=1)
root.geometry("800x500")

def delvægt():
    cursor.execute('SELECT top 1 * FROM [weightCollector].[dbo].[Fasterholt] order by ID desc')
    row = cursor.fetchone()
    cursor.execute('insert into [weightCollector].[dbo].[Fasterholt] (value,partvalue,partboo) values ('+row.value+','+row.partvalue+',1)')
    cursor.commit()
    print("Delvægt sat!")

def reset():
    cursor.execute('insert into [weightCollector].[dbo].[Fasterholt] (value,partvalue,partboo) values ('"0"','"0"',0)')
    cursor.commit()
    print("Resat!")

w1Str = StringVar()
w2Str = StringVar()
w3Str = StringVar()
w4Str = StringVar()
w1 = Label(root, textvar=w1Str, font="Helvetica 250 bold", fg="red")
w1.grid(row=1, sticky=N+W+E)
w2 = Label(root, textvar=w2Str, font="Helvetica 250 bold", fg="blue")
w2.grid(row=2, sticky=N+W+E)
w3 = Button(root, text="Delvægt", command=delvægt)
w3.grid(row=2, column=2, sticky=S+E)
w4 = Button(root, text="Reset", command=reset)
w4.grid(row=2, column=3, sticky=S+E,padx=(10, 10))
w5 = Label(root, textvar=w3Str)
w5.grid(row=4, column=2, sticky=S+E)



def serialRead():
    raw = ser.readline().decode('utf-8')
    seq = ''.join(str(v) for v in raw if v in "1234567890")
    result = int
    if len(seq) > 3:
        result = int(float(seq) * 0.000000000001)
        cursor.execute('SELECT top 1 * FROM [weightCollector].[dbo].[Fasterholt] order by ID desc')
        row = cursor.fetchone()

        if not row:
            cursor.execute('insert into [weightCollector].[dbo].[Fasterholt] (value,partvalue,partboo) values ('"0"','"0"',0)')
            cursor.commit()
            print("No records... Fixed")
            cursor.execute('SELECT top 1 * FROM [weightCollector].[dbo].[Fasterholt] order by ID desc')
            row = cursor.fetchone() 
                   
        if row.partboo is True:
            sqlTxt = "insert into [weightCollector].[dbo].[Fasterholt] (value,partvalue,partboo) values ('"+str(result)+"','"+row.partvalue+"',1)"
        else:
            sqlTxt = "insert into [weightCollector].[dbo].[Fasterholt] (value,partvalue,partboo) values ('"+str(result)+"','"+str(result)+"',0)"

        cursor.execute(sqlTxt)
        cursor.commit()
        w1Str.set(result)
        w3Str.set("(Vægt/Delvægt): "+str(result)+" / "+str(row.partvalue).strip()+" Raw: "+str(seq))

        if row.partvalue is not "None":	
            w2Str.set(int(float(row.partvalue)))
            
        seq = ''
    root.update_idletasks()
    root.after(100,serialRead)

root.after(0,serialRead)
root.mainloop()