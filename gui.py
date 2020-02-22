from Tkinter import *
import tkMessageBox
import tkFont
import ttk
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.output(35, GPIO.LOW) #Produkt A
GPIO.output(37, GPIO.LOW) #Produkt B
GPIO.setup(33, GPIO.IN) #Station B fertig
GPIO.setup(31,GPIO.IN)  #Station C fertig
GPIO.setup(29,GPIO.IN)  #Station D fertig
GPIO.setup(32,GPIO.IN)  #Station E fertig
GPIO.setup(40, GPIO.IN) #Prozess fertig

lastState = 100;

win = Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
smallFont = tkFont.Font(family = 'Helvetica', size = 18, weight = 'bold')

def productA():
    if lastState == 100:
        print("Product A selected and GPIO35 set to HIGH")
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(37,GPIO.LOW)
        productAbutton["text"] = "Produkt A"
    
def productB():
    if lastState == 100:
        print("Product B selected and GPIO37 set to HIGH")
        GPIO.output(37,GPIO.HIGH)
        GPIO.output(35,GPIO.LOW)
        productBbutton["text"] = "Produkt B"

def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    win.quit()  


win.title("Produktwahl")
win.geometry('800x480')

#product buttons
productAbutton = Button(win, text = "Produkt A", font = myFont, command = productA, height = 2, width =8, bg='#fcba03')
productAbutton.pack(pady=10)
productBbutton = Button(win, text = "Produkt B", font = myFont, command = productB, height = 2, width =8, bg='#1363a1' )
productBbutton.pack(pady=10)

#progressbar
progressbar = ttk.Progressbar(orient=HORIZONTAL, length=200, mode='determinate')
progressbar.pack(side=TOP,pady=10)
#progressbar.start()




try:
    while 1:
        win.update_idletasks()
        win.update()
        
        #process finished - reset everything
        if GPIO.input(40) == GPIO.HIGH and lastState != 100:
            #reset progressbar for next process
            progressbar.stop()
            print("Finished")
            #reset product choices
            GPIO.output(35,GPIO.LOW) 
            GPIO.output(37,GPIO.LOW)
            tkMessageBox.showinfo('Produktwahl', 'Produkt fertig')
            lastState = 100
        
        if GPIO.input(33) == GPIO.HIGH and lastState !=25:
            progressbar.stop()
            progressbar.step(25)
            print("25")
            lastState = 25
        if GPIO.input(31) == GPIO.HIGH and lastState !=50:
            progressbar.stop()
            progressbar.step(50)
            lastState = 50
            print("50")
        if GPIO.input(29) == GPIO.HIGH and lastState !=75:
            progressbar.stop()
            progressbar.step(75)
            print("75")
            lastState = 75
        if GPIO.input(32) == GPIO.HIGH and lastState !=99:
            progressbar.stop()
            progressbar.step(99)
            print("99")
            lastState = 99
        
except KeyboardInterrupt:
   GPIO.cleanup()
   
