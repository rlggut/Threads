from tkinter import *
import threading
import time
import math

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Осцилограмма")
        self.canvasW = 400
        self.canvasH = 400
        self.window.geometry("400x400")
        self.frame = Frame(self.window)
        self.frame.grid()
        self.x=self.canvasW//2
        self.y=self.canvasH//2
        self.r=3
        self.dist=197
        self.alpX=0
        self.t=0
        self.freqT=100
        self.freqX=2
        self.freqY=1

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0)

        self.threadDraw=threading.Thread(target=self.__Draw, args=())
        self.threadDraw.start()

        self.window.mainloop()
    def __Draw(self):
        dX=self.dist*math.sin(self.freqX*math.pi*(self.t/self.freqT)+self.alpX)+self.x
        dY=self.dist*math.sin(self.freqY*math.pi*(self.t/self.freqT))+self.y
        self.canvas.create_oval(dX-self.r,dY-self.r,dX+self.r,dY+self.r, fill='grey70')
        self.t+=1
        time.sleep(0.03)
        self.__Draw()


app=App()