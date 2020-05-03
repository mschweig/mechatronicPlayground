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
ser = serial.Serial ("/dev/ttyS0",9600)


GPIO.setmode(GPIO.BOARD)


win = Tk()


myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
smallFont = tkFont.Font(family = 'Helvetica', size = 18, weight = 'bold')

def sel():
   selection = "Value = " + str(fio2Var.get())
   label.config(text = selection)

def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    win.quit()
    
win.title("StuVent")
win.geometry('800x480')

#FIO2 Scale
fio2Var = DoubleVar()
fio2Scale = Scale(win, from_=0, to = 100,variable = fio2Var, orient = HORIZONTAL,length = 400, width = 50, label = "FiO2", activebackground = "red")
fio2Scale.pack(anchor = CENTER)

#Pressure Scale
pressureVar = DoubleVar()
pressureScale = Scale(win, from_=0, to = 100,variable = pressureVar, orient = HORIZONTAL, length = 400, width = 50, label = "Pressure",activebackground = "red")
pressureScale.pack(anchor=CENTER)

#BPM
bpmVar = DoubleVar()
pressureScale = Scale(win, from_=0, to = 100,variable = bpmVar, orient = HORIZONTAL, length = 400, width = 50, label = "BPM", activebackground = "red")
pressureScale.pack(anchor=CENTER)

#PEEP
peepVar = DoubleVar()
pressureScale = Scale(win, from_=0, to = 100,variable = peepVar, orient = HORIZONTAL, length = 400, width = 50, label = "PEEP", activebackground = "red")
pressureScale.pack(anchor=CENTER)

label = Label(win)
label.pack()


#progressbar
progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
progressbar.pack(side=TOP,pady=10)
progressbar.start()


#read data from serial port in a new thread
def read_from_port(ser):
    while (ser.inWaiting() > 0):

        while True:
           print("received data via serial: ")
           serialData = ser.readline().decode()
           print(serialData)
           
#start a new thread for serial readings
thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

serialData = 0

try:
    while 1:
        win.update_idletasks()
        win.update()
        
except KeyboardInterrupt:
   GPIO.cleanup()
   
