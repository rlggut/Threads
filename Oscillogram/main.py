from tkinter import *
import threading
import time
import math

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Фигуры Лиссажу")
        self.canvasW = 400
        self.canvasH = 400
        self.window.geometry("680x400")
        self.frame = Frame(self.window)
        self.frame.grid()
        self.x=self.canvasW//2
        self.y=self.canvasH//2
        self.r=3
        self.dist=195
        self.alpX=0
        self.timeAmpl=100
        self.freqX=1
        self.freqY=1
        self.pointNum=10

        self.canvas = Canvas(self.frame, height=self.canvasH, width=self.canvasW, bg='white')
        self.canvas.grid(column=0, row=0, rowspan=12)
        self.__restart()

        self.lblPoints = Label(self.frame, text="Количество точек для отрисовки")
        self.lblPoints.grid(column=1, row=0, columnspan=2)
        self.pointNumSpin = Spinbox(self.frame, from_ =10, to_=195, width=5, command=self.__changePointsNum)
        self.pointNumSpin.grid(column=3, row=0)

        self.lblFreq = Label(self.frame, text="Отношение частот:")
        self.lblFreq.grid(column=1, row=1)
        self.freqXSpin = Spinbox(self.frame, from_ =1, to_=5, width=3, command=self.__changeFreq)
        self.freqXSpin.grid(column=2, row=1)
        lblCommon = Label(self.frame, text="к")
        lblCommon.grid(column=3, row=1)
        self.freqYSpin = Spinbox(self.frame, from_ =1, to_=5, width=3, command=self.__changeFreq)
        self.freqYSpin.grid(column=4, row=1)

        self.lblAlp = Label(self.frame, text="Сдвиг фаз (в градусах):")
        self.lblAlp.grid(column=1, row=2, columnspan=2)
        self.alpSpin = Spinbox(self.frame, from_ =0, to_=180, width=5, command=self.__changeFreq)
        self.alpSpin.grid(column=3, row=2)

        self.threadDraw=threading.Thread(target=self.__needDraw, args=())
        self.threadDraw.start()

        self.window.mainloop()

    def __restart(self):
        self.canvas.delete("all")
        self.t=0
        self.points=[]

    def __changeFreq(self):
        self.freqX=int(self.freqXSpin.get())
        self.freqY=int(self.freqYSpin.get())
        self.alpX=int(self.alpSpin.get())
        #self.__restart()
    def __changePointsNum(self):
        self.pointNum=int(self.pointNumSpin.get())
    def __needDraw(self):
        while(True):
            time.sleep(0.03)
            self.__Draw()
    def __Draw(self):
        dX= self.dist * math.sin(self.freqX * math.pi * (self.t / self.timeAmpl) + math.pi * (self.alpX / 180)) + self.x
        dY= self.dist * math.sin(self.freqY * math.pi * (self.t / self.timeAmpl)) + self.y
        self.points.append(self.canvas.create_oval(dX-self.r,dY-self.r,dX+self.r,dY+self.r, fill='grey70'))
        while(len(self.points)>self.pointNum):
            self.canvas.delete(self.points[0])
            self.points.pop(0)
        self.t=(self.t+1)%(2*self.timeAmpl)


app=App()