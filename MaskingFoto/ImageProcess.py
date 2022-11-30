from tkinter import *
from PIL import Image, ImageTk
from Matrix import *

def maskedImageMatrix(image, matrX, matrY, edge):
    if not(isinstance(image, Image.Image)):
        return False
    if not(isinstance(matrX, Matrix)):
        return False
    if not(isinstance(matrY, Matrix)):
        return False
    res = Image.new('RGB', (image.width, image.height), (0,0,0))
    for y in range(1,image.height-1):
        for x in range(1,image.width-1):
            gX = 0
            gY = 0
            for j in range(-1,2):
                for i in range(-1,2):
                    value = image.getpixel((x+i, y+j))
                    if(isinstance(value,tuple)):
                        value=((value[0]+value[1]+value[2])/3)
                    gX += matrX.getMatrXY(i+1,j+1)*value
                    gY += matrY.getMatrXY(i+1,j+1)*value
            degree=pow(gX*gX+gY*gY,0.5)
            if(degree> edge):
                res.putpixel((x,y), (255,255,255))
    return res

def compareImage(image1, image2):
    if not(isinstance(image1, Image.Image)):
        return False
    if not(isinstance(image2, Image.Image)):
        return False
    width = min(image1.width,image2.width)
    height = min(image1.height,image2.height)
    diffNums = 0
    for y in range(height):
        for x in range(width):
            if(image1.getpixel((x,y))!=image2.getpixel((x,y))):
                diffNums+=1
    return diffNums

def compareImageProc(image1, image2):
    diff = compareImage(image1, image2)
    size = max(image1.height*image1.width, image2.height*image2.width)
    return (100*(size-diff))/size