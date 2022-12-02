from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from Matrix import *
from ImageProcess import *
import re
import time
import threading
import concurrent.futures

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Маскирование изображения")
        self.canvasW = 200
        self.canvasH = 200
        size=""+str(int(self.canvasW*7.5))+"x"+str(int(self.canvasH *2.45))
        self.window.geometry(size)
        self.frame = Frame(self.window)
        self.frame.grid()
        self.image = Image.new('RGB', (self.canvasW, self.canvasH), (240,240,240))
        self.photo = ImageTk.PhotoImage(self.image)

        self.lblLoad = Label(self.frame, text="Выберите изображение")
        self.lblLoad.grid(column=0, row=0,columnspan=3)
        self.btnLoad = Button(self.frame, text="...", command=self.__clickedLoading)
        self.btnLoad.grid(column=3, row=0)
        self.lblChoosed = Label(self.frame, text="FileName.(png/jpg)")
        self.lblChoosed.grid(column=0, row=1, columnspan=3)
        self.filename = ""

        self.lblMatrX = Label(self.frame, text="Матричный фильтр X")
        self.lblMatrX.grid(column=0, row=2, columnspan=3)

        self.dataX=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=0+i, row=3+j)
            if(i==0):
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '1')
            elif(i==1):
                dataColumn[0].insert(0, '-2')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '2')
            else:
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '1')
            self.dataX.append(dataColumn)
        self.lblMatrY = Label(self.frame, text="Матричный фильтр Y")
        self.lblMatrY.grid(column=0, row=6, columnspan=3)

        self.dataY=[]
        for i in range(3):
            dataColumn = []
            for j in range(3):
                dataColumn.append(Entry(self.frame, width=5))
                dataColumn[j].grid(column=0+i, row=7+j)
            if (i == 0):
                dataColumn[0].insert(0, '-1')
                dataColumn[1].insert(0, '-2')
                dataColumn[2].insert(0, '-1')
            elif (i == 1):
                dataColumn[0].insert(0, '0')
                dataColumn[1].insert(0, '0')
                dataColumn[2].insert(0, '0')
            else:
                dataColumn[0].insert(0, '1')
                dataColumn[1].insert(0, '2')
                dataColumn[2].insert(0, '1')
            self.dataY.append(dataColumn)

        self.lblEdge = Label(self.frame, text="Значение граничного детектора")
        self.lblEdge.grid(column=0, row=10, columnspan=3)
        self.edgeSpin = Spinbox(self.frame, from_ =0, to_=300, width=5, command=self.__getMaskPic)
        self.edgeSpin.grid(column=3, row=10)
        self.edge = 100
        self.edgeSpin.delete(0, len(self.edgeSpin.get()))
        self.edgeSpin.insert(0, str(self.edge))

        self.btnRecalc = Button(self.frame, text="Пересчет", command=self.__getMaskPic, state=DISABLED)
        self.btnRecalc.grid(column=0, row=11, columnspan=3)

        self.lblOrig = Label(self.frame, text="Исходное изображение")
        self.lblOrig.grid(column=4, row=0)
        self.canvasOrig = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_image = self.canvasOrig.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvasOrig.grid(column=4, row=1, rowspan=12)

        self.canvasThreads=[]
        self.с_imageThreads=[]
        self.lblThreads=[]
        self.imageMaskedTh=[]
        self.photoTh=[]
        for i in range(4):
            self.imageMaskedTh.append(self.image)
            self.photoTh.append(self.photo)
            self.canvasThreads.append(Canvas(self.frame, height=self.canvasH, width=self.canvasW))
            self.с_imageThreads.append(self.canvasThreads[i].create_image(0, 0, anchor='nw', image=self.photoTh[i]))
            self.canvasThreads[i].create_line(0, 0, self.canvasW, self.canvasH)
            self.canvasThreads[i].create_line(0, self.canvasH, self.canvasW, 0)
            self.canvasThreads[i].grid(column=5+i, row=1, rowspan=12)
            self.lblThreads.append(Label(self.frame, text=str(i+1)+" -й поток"))
            self.lblThreads[i].grid(column=5+i, row=0)

        self.lblSumm=Label(self.frame, text="Сложение результатов")
        self.lblSumm.grid(column=9, row=0)
        self.canvasSumm = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageSumm = self.canvasSumm.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvasSumm.create_line(0, 0, self.canvasW, self.canvasH)
        self.canvasSumm.create_line(0, self.canvasH, self.canvasW, 0)
        self.canvasSumm.grid(column=9, row=1,rowspan=12)

        self.lblUniq=Label(self.frame, text="Одним потоком")
        self.lblUniq.grid(column=4, row=13)
        self.canvasOne = Canvas(self.frame, height=self.canvasH, width=self.canvasW)
        self.с_imageMasked = self.canvasOne.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvasOne.create_line(0, 0, self.canvasW, self.canvasH)
        self.canvasOne.create_line(0, self.canvasH, self.canvasW, 0)
        self.canvasOne.grid(column=4, row=14,rowspan=12)

        self.lblTimeUniq=Label(self.frame, text="Время на один поток: --")
        self.lblTimeUniq.grid(column=5, row=13)
        self.lblTimeSumm=Label(self.frame, text="Время на потоки:     --")
        self.lblTimeSumm.grid(column=5, row=14)

        self.window.mainloop()

    def __clickedLoading(self):
        file = filedialog.askopenfilename(filetypes=[("Image (png/jpg)", ("*.png", "*.jpg"))])
        if(file==""):
            return False
        self.btnRecalc["state"] = "normal"
        self.filename = file
        self.image = Image.open(file)
        self.image.load()
        pattern = '[^\/]+\.\D+'
        file = re.search(pattern,file).group(0)
        self.lblChoosed.configure(text=file)
        factorW = self.canvasW / self.image.width
        factorH = self.canvasH / self.image.height
        factor=min(factorW, factorH)
        self.imageW=int(factor * self.image.width)
        self.imageH=int(factor * self.image.height)
        self.photo = ImageTk.PhotoImage(self.image.resize((self.imageW, self.imageH)))
        self.с_image = self.canvasOrig.create_image(0, 0, anchor='nw', image=self.photo)

        self.imageGrey = self.__getGrey()
        self.imageGrey.load()
        self.photoGrey = ImageTk.PhotoImage(self.imageGrey)
        self.__getMaskPic()
    def __ThreadResearch(self, n):
        self.canvasThreads[n].delete("all")
        w=self.imageGrey.width/2
        h=self.imageGrey.height/2
        x1 = int((n%2)*w)
        y1 = int((n//2)*h)
        x2 = int((n%2+1)*w)
        y2 = int(((n//2)+1)*h)
        crops = self.imageGrey.crop((x1, y1, x2, y2))
        self.imageMaskedTh[n] = maskedImageMatrix(crops, self.matrX, self.matrY, self.edge)
        self.photoTh[n] = ImageTk.PhotoImage(self.imageMaskedTh[n].resize((self.imageW//2, self.imageH//2)))
        self.с_imageThreads[n] = self.canvasThreads[n].create_image(0, 0, anchor='nw', image=self.photoTh[n])
        self.canvasSumm.create_image(int((n%2)*self.imageW/2), int((n//2)*self.imageH/2), anchor='nw', image=self.photoTh[n])
        self.countThr+=1
        if(self.countThr==4):
            endThread = time.time() - self.startThread
            self.lblTimeSumm['text']='Время на потоки: '+str(endThread)

    def __getMaskPic(self):
        self.canvasOne.delete("all")
        if(self.filename==""):
            return False
        if(re.match("[^0-9]",self.edgeSpin.get())):
            self.edgeSpin.delete(0, len(self.edgeSpin.get()))
            self.edgeSpin.insert(0, str(self.edge))
        self.edge=int(self.edgeSpin.get())
        self.__getMatrXY()
        startOne = time.time()
        self.imageMasked = maskedImageMatrix(self.imageGrey, self.matrX, self.matrY, self.edge)
        self.photoMasked = ImageTk.PhotoImage(self.imageMasked.resize((self.imageW, self.imageH)))
        self.с_imageMasked = self.canvasOne.create_image(0, 0, anchor='nw', image=self.photoMasked)
        endOne = time.time() - startOne
        self.lblTimeUniq['text']='Время на поток: '+str(endOne)

        self.canvasSumm.delete("all")
        self.startThread = time.time()
        self.countThr=0
        threads=[]
        for i in range(4):
            threads.append(threading.Thread(target=self.__ThreadResearch, args=(i,)))
            threads[i].start()
    def __getMatrXY(self):
        self.matrX = Matrix(3, 3)
        matr = []
        for j in range(3):
            column = []
            for i in range(3):
                if (self.dataX[i][j].get() == '') or not (re.match('\-?\d+(\.\d+)?', self.dataX[i][j].get())) \
                        or (re.search('[^0-9\.\-]', self.dataX[i][j].get())):
                    self.dataX[i][j].delete(0, len(self.dataX[i][j].get()))
                    self.dataX[i][j].insert(0, '0')
                column.append(float(self.dataX[i][j].get()))
            matr.append(column)
        self.matrX.setData(matr)
        self.matrY = Matrix(3, 3)
        matr = []
        for j in range(3):
            column = []
            for i in range(3):
                column.append(float(self.dataY[i][j].get()))
            matr.append(column)
        self.matrY.setData(matr)

    def __getGrey(self):
        res = self.image.convert("L")
        return res
    def __getGreyOwn(self):
        res = Image.new('RGB', (self.image.width, self.image.height), (0,0,0))
        for y in range(self.image.height):
            for x in range(self.image.width):
                value = self.image.getpixel((x,y))
                greyCol = int(value[0]*0.3+value[1]*0.59+value[2]*0.11)
                res.putpixel((x,y), (greyCol,greyCol,greyCol))
        return res

app=App()