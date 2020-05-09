from Tkinter import *
import tkMessageBox
import tkFont
import ttk
import RPi.GPIO as GPIO
import time
import serial
import threading
import Queue

#Start Serial Communication with Arduino Mega in another thread
ser = serial.Serial ("/dev/ttyACM1",9600,timeout=0, writeTimeout=0)



GPIO.setmode(GPIO.BOARD)


win = Tk()


myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
smallFont = tkFont.Font(family = 'Helvetica', size = 18, weight = 'bold')

def fio2Sel(event):
   selection = "FiO2 Value = " + str(fio2Var.get())
   label.config(text = selection)
   #Write here data to Arduino
   ser.write(str(fio2Var.get()))
   
def pressureSel(event):
   selection = "Pressure Value = " + str(pressureVar.get())
   label.config(text = selection)
   #Write here data to Arduino
   ser.write(str(pressureVar.get()))
   
def bpmSel(event):
   selection = "BPM Value = " + str(bpmVar.get())
   label.config(text = selection)
   #Write here data to Arduino
   ser.write(str(bpmVar.get()))
   
def tidalSel(event):
   selection = "Tidal Value = " + str(tidalVar.get())
   label.config(text = selection)
   #Write here data to Arduino
   ser.write(str(tidalVar.get()))
   
def modeSel():
   selection = "Selected Mode: " + str(radioVar.get())
   ser.write(str(radioVar.get()))
   label.config(text = selection)
   #Write here data to Arduino
   
   
   
def controlSel():
   selection = "Selected Control Mode: " + str(controlVar.get())
   label.config(text = selection)
   #Write here data to Arduino
   ser.write(str(controlVar.get()))


def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    win.quit()
    
win.title("StuVent")
win.geometry('800x480')

#FIO2 Scale
fio2Var = DoubleVar()
fio2Scale = Scale(win, from_=0, to = 100,variable = fio2Var, orient = HORIZONTAL,length = 400, width = 50, label = "FiO2", activebackground = "red", command = fio2Sel)
fio2Scale.pack(anchor = CENTER)

#Pressure Scale
pressureVar = DoubleVar()
pressureScale = Scale(win, from_=0, to = 100,variable = pressureVar, orient = HORIZONTAL, length = 400, width = 50, label = "Inspiriatory Pressure",activebackground = "red", command = pressureSel)
pressureScale.pack(anchor=CENTER)

#BPM
bpmVar = DoubleVar()
bpmScale = Scale(win, from_=0, to = 100,variable = bpmVar, orient = HORIZONTAL, length = 400, width = 50, label = "BPM", activebackground = "red", command = bpmSel)
bpmScale.pack(anchor=CENTER)

#Tidal Volume
tidalVar = DoubleVar()
tidalScale = Scale(win, from_=0, to = 100,variable = tidalVar, orient = HORIZONTAL, length = 400, width = 50, label = "Tidal Volume", activebackground = "red", command = tidalSel)
tidalScale.pack(anchor=CENTER)

#Radio Buttons for Modes
radioVar = IntVar()
controlVar = IntVar()
R1 = Radiobutton(win, text="Assited Ventilation", variable=radioVar, value=1, command=modeSel, height = 2, activebackground = "red")
R1.pack(anchor = CENTER)

R2 = Radiobutton(win, text="Forced/Intubated Ventilation Mode", variable=radioVar, value=2,command=modeSel, height = 2, activebackground = "red")
R2.pack(anchor = CENTER)

R3 = Radiobutton(win, text="Volume Controlled", variable=controlVar, value=3,command=controlSel, height = 2, activebackground = "red")
R3.pack(anchor = CENTER)

R4 = Radiobutton(win, text="Pressure Controlled", variable=controlVar, value=4,command=controlSel,height = 2, activebackground = "red")
R4.pack(anchor = CENTER)

label = Label(win)
label.pack()


#progressbar
progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
progressbar.pack(side=TOP,pady=10)
progressbar.start()

#Arduino RCV
serialText = Text(win, height=2, width=30, background = "white")
serialText.pack()
serialText.insert(END, "Test")

#read data from serial port function
def readSerial(win):

    while(ser.inWaiting() > 0):
        
        print("received data via serial: ")
        serialData = ser.readline().decode()
        serialText.insert(END, serialData)
        serialText.see(END)
        serialText.update_idletasks()
        print(serialData)
    win.after(500, readSerial, win)
           
#start a new thread for serial readings
#thread = threading.Thread(target=read_from_port, args=(ser,))
#thread.setDaemon(True)
#thread.start()

readSerial(win)
win.mainloop()
        

   
