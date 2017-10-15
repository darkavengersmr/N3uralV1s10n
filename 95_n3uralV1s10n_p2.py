#!/usr/bin/env python3

from ev3dev.ev3 import *
import pygame
import time
import pygame.camera
from random import random
from PIL import Image, ImageDraw, ImageFont

lcd = Screen()
btn = Button()

res = 16

S1 = TouchSensor("in1")
S2 = TouchSensor("in4")

buf = [ [0] * res for i in range(res)]

class number:
    def __init__(self, n):
        self.name = n
        self.sum = 0
        self.picture = [ [0] * res for i in range(res)]
               

myNumbers = []

def camera_update(x):
    for i in range(x):
         
        image = cam.get_image()
        
        image = pygame.transform.scale(image,(res,res))
        image2buf(image)
        for i in range(res):
            for j in range(res):
                if buf[i][j] == 0:
                    lcd.draw.rectangle(((i*8+25), j*8, (i*8+25)+7, j*8+7),fill='white')
                else:
                    lcd.draw.rectangle(((i*8+25), j*8, (i*8+25)+7, j*8+7),fill='black')
        lcd.update()

def write(n):
    f = ImageFont.truetype('FreeMonoBold.ttf', 175)
    lcd.draw.text((30,-15), str(n), font=f)
    lcd.update()

def image2buf(surf):
    width, height = surf.get_size() 
    for y in range(height): 
        for x in range(width): 
            red, green, blue, alpha = surf.get_at((x, y)) 
            L = 0.3 * red + 0.59 * green + 0.11 * blue
            if L > 100:
                buf[x][y] = 0
            else:
                buf[x][y] = 1
      
pygame.init()
pygame.camera.init()
cameras = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cameras[0])
cam.start()

lcd.clear()

f = ImageFont.truetype('FreeMonoBold.ttf', 25)
lcd.draw.text((0,50), "N3uralV1s10n", font=f)
lcd.update()
Sound.speak("neural vision programm 2").wait()
time.sleep(2)
lcd.clear()

str1 = "please put"
str2 = "first object"
str3 = "and press enter"
f = ImageFont.truetype('FreeMonoBold.ttf', 25)
lcd.draw.text((0,30), str1, font=f)
lcd.draw.text((0,55), str2, font=f)
f = ImageFont.truetype('FreeMonoBold.ttf', 20)
lcd.draw.text((0,80), str3, font=f)
lcd.update()
Sound.speak("please put first object and press enter").wait()

while(True):
    if(btn.enter): break
lcd.clear()

while(True):
    camera_update(15)
     
    image = cam.get_image()
    
    image = pygame.transform.scale(image,(res,res))
    image2buf(image)
        
    for i in range(res):
        for j in range(res):
            if buf[i][j] == 0:
                lcd.draw.rectangle(((i+25)*8, j*8, (i+25)*8+7, j*8+7),fill='white')
            else:
                lcd.draw.rectangle(((i+25)*8, j*8, (i+25)*8+7, j*8+7),fill='black')

    lcd.update()
    
    for o in myNumbers:
        o.sum = 0
    for o in myNumbers:    
        for i in range(res):
            for j in range(res):
                o.sum += buf[i][j] * o.picture[i][j]

    max_sum = -100000
    
    for num in myNumbers:
        if num.sum > max_sum:
            max_sum = num.sum
            tmp_obj = num
    
    lcd.clear()
    
    if(len(myNumbers)!=0): 
        write(tmp_obj.name)
    
        Sound.speak("It is "+str(tmp_obj.name)).wait()
    else: Sound.speak("I do not know object").wait()
    while(True):
        if(S1.value() and len(myNumbers)!=0): break
        if(S2.value() and len(myNumbers)!=0): break
        if(btn.enter or len(myNumbers)==0): break
    a=0
    if(S1.value() and len(myNumbers)!=0): 
        Sound.speak("ok yes").wait()
        a = 1
    elif(S2.value() and len(myNumbers)!=0): 
        Sound.speak("no no").wait()
        a = -1
    else: 
        Sound.speak("new object").wait()
        time.sleep(1)
        i = 48
        while(True):
            if(btn.enter): break
            if(btn.right): i+=1
            if(btn.left): i-=1
            if(i>90): i=48
            if(i<48): i=90
            if(i>=58 and i<=64): 
                if(btn.right): i=65
                else: i=57
            lcd.clear()
            
            time.sleep(0.15)
            write(chr(i))
        myNumbers.append(number(chr(i)))
        Sound.speak("new object it is" + chr(i)).wait()
        for i in range(res):
            for j in range(res):
                myNumbers[len(myNumbers)-1].picture[i][j] = buf[i][j]
    if(a!=0):
        for i in range(res):
            for j in range(res):
                if(buf[i][j] == 1):
                    tmp_obj.picture[i][j] += a
   
    Sound.speak("put a new object and press enter").wait()
    while(True):
        if(btn.enter): break
        if(btn.backspace): 
           Sound.speak("Exit programm").wait()
           exit()
    lcd.clear()

cam.stop()   

