import os
import os.path
import sys
import cv2
import math
import pynput
import time
import random
import numpy as np
from operator import itemgetter
from pynput.keyboard import Key, Controller

def draw(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 50, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=3, minDist=100, param1=200, param2=150, minRadius=100, maxRadius=200)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    output = edges_bgr

    if circles is not None and len(circles[0,:]) >= 2:    
        circles = np.uint16(np.around(circles))
        
        #Classificando maiores circulos
        sorted_circles = sorted(circles[0], key = itemgetter(2), reverse=1)
        circle1 = sorted_circles[0]
        circle2 = sorted_circles[1]
        
        #Calculando inclinação da reta
        deltaY = int(circle2[1]) - int(circle1[1])
        deltaX = int(circle2[0]) - int(circle1[0])

        if(deltaX == 0):
            m = deltaY
        elif(deltaY == 0):
            m = deltaX
        else:
            m = deltaY / deltaX

        radians = math.atan(m)
        degrees = round(math.degrees(radians))

        defaultColor = (255, 255, 255)
        circleColor = (0, 255, 0)
        lineColor = (255, 0, 0)

        #Círculo 1
        cv2.circle(output, (circle1[0], circle1[1]), circle1[2], circleColor, 2)
        cv2.circle(output, (circle1[0], circle1[1]), 5, circleColor, 3)
        area1 = round(math.pi * circle1[2] ** 2, 2)
        cv2.putText(output, "Area do circulo 1: " + str(area1) + "cm", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, defaultColor, 2, cv2.LINE_AA)

        #Círculo 2
        cv2.circle(output, (circle2[0], circle2[1]), circle2[2], circleColor, 2)
        cv2.circle(output, (circle2[0], circle2[1]), 5, circleColor, 3)
        area2 = round(math.pi * circle2[2] ** 2, 2)
        cv2.putText(output, "Area do circulo 2: " + str(area2) + "cm", (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, defaultColor, 2, cv2.LINE_AA)

        #Linha entre os círculos
        cv2.line(output, (circle1[0], circle1[1]), (circle2[0], circle2[1]), lineColor, 5)

        #Inserindo grau de inclinação
        cv2.putText(output, str(degrees) + " graus de inclinacao", (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, defaultColor, 2, cv2.LINE_AA)
        
        emulateKey(degrees, output)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    return output

def emulateKey(degrees, output):
    keys = [
        Key.right,
        Key.left
    ]

    keyboard = Controller()

    defaultColor = (255, 255, 255)

    #Tem uma zona morta de 20 graus de inclinação
    if degrees < -20:
        cv2.putText(output, "Tecla acionada: " + str(keys[0]), (25, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, defaultColor, 2, cv2.LINE_AA)
        keyboard.press(keys[0])
        time.sleep(0.1)
        keyboard.release(keys[0])
    elif degrees > 20:
        cv2.putText(output, "Tecla acionada: " + str(keys[1]), (25, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, defaultColor, 2, cv2.LINE_AA)
        keyboard.press(keys[1])
        time.sleep(0.1)
        keyboard.release(keys[1])

cv2.namedWindow("preview")
video = cv2.VideoCapture(0)

if video.isOpened():
    isOpened, frame = video.read()
else:
    isOpened = False

while isOpened:
    img = draw(frame)
    cv2.imshow("preview", img)

    isOpened, frame = video.read()
    key = cv2.waitKey(20)
    if key == 27: 
        break

cv2.destroyWindow("preview")
video.release()



