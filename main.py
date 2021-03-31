import cv2
from matplotlib import pyplot as plt
import numpy as np
import os, sys, os.path
import math
from pynput.keyboard import Key, Controller
import pynput
import time
import random
from operator import itemgetter

def draw(img):
    #img = cv2.imread('circulos.png')
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray, 50, 150)
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=3, minDist=100, param1=200, param2=200, minRadius=0, maxRadius=50)
    #circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=3, minDist=100, param1=200, param2=200, minRadius=0, maxRadius=500)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    output = edges_rgb

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

        #Círculo 1
        cv2.circle(output, (circle1[0], circle1[1]), circle1[2], (0, 255, 0), 2)
        cv2.circle(output, (circle1[0], circle1[1]), 5, (0, 0, 255), 3)

        #Círculo 2
        cv2.circle(output, (circle2[0], circle2[1]), circle2[2], (0, 255, 0), 2)
        cv2.circle(output, (circle2[0], circle2[1]), 5, (0, 0, 255), 3)

        #Linha entre os círculos
        cv2.line(output, (circle1[0], circle1[1]), (circle2[0], circle2[1]), (255, 0, 0), 5)

        #Inserindo grau de inclinação
        cv2.putText(output, str(degrees), (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        emulateKey(degrees, output)

    return output

def emulateKey(degrees, output):
    keys = [
        Key.right,
        Key.left
    ]

    keyboard = Controller()

    if degrees < -20:
        cv2.putText(output, str(keys[0]), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        print('Tecla: ', keys[0])
        keyboard.press(keys[0])
        time.sleep(0.1)
        keyboard.release(keys[0])
    elif degrees > 20:
        cv2.putText(output, str(keys[1]), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        print('Tecla: ', keys[1])
        keyboard.press(keys[1])
        time.sleep(0.1)
        keyboard.release(keys[1])

#plt.imshow(draw(None))
#plt.show()

cv2.namedWindow("Game")
#video = cv2.VideoCapture("circulos.mp4")
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if video.isOpened():
    isOpened, frame = video.read()
else:
    isOpened = False

while isOpened:
    img = draw(frame)
    cv2.imshow("Game", img)

    isOpened, frame = video.read()
    key = cv2.waitKey(20)
    if key == 27: 
        break

cv2.destroyAllWindows()
video.release()



