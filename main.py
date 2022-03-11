from collections import deque

import numpy as np
import cv2
from cv2 import setTrackbarPos

#Below functions are called when sliding trackbar.
#When sliding red trackbar, it sets the marker as red, making green and blue 0
def setValuesRed(x):
    setTrackbarPos("Green", "Marker Color", 0)
    setTrackbarPos("Blue", "Marker Color", 0)
def setValuesGreen(x):
    setTrackbarPos("Red", "Marker Color", 0)
    setTrackbarPos("Blue", "Marker Color", 0)
def setValuesBlue(x):
    setTrackbarPos("Green", "Marker Color", 0)
    setTrackbarPos("Red", "Marker Color", 0)

# Code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255

#Below codes creates trackbar in a window called "Marker Color"
cv2.namedWindow("Marker Color")
cv2.createTrackbar("Red", "Marker Color",0, 1, setValuesRed)
cv2.createTrackbar("Green", "Marker Color", 0, 1, setValuesGreen)
cv2.createTrackbar("Blue", "Marker Color",0, 1, setValuesBlue)
setTrackbarPos("Blue", "Marker Color", 1)                                   #Sets marker color as blue by default

#Array which holds colors
colors = [(255, 0, 0), (0, 255, 0),(0, 0, 255), (0, 255, 255)]

colorIndex = 0

#Below array "kernel" is used for morphology operations
kernel = np.ones((5, 5), np.uint8)

#Marks color points in the array
red_index = 0
green_index = 0
blue_index = 0
yellow_index = 0

#Setting queues for storing pixel values of each colors
rpoints = [deque(maxlen = 1024)]
gpoints = [deque(maxlen = 1024)]
bpoints = [deque(maxlen = 1024)]
ypoints = [deque(maxlen = 1024)]

cap = cv2.VideoCapture(0)                                          #Camera initialization

while(True):
    ret, frame = cap.read()                                         #Video frame
    frame = cv2.flip(frame, 1)                                      #Flipping the camera as it shows mirror image

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                    #Converts the frame to HSV color space

    #Getting the values of trackbar
    red = cv2.getTrackbarPos("Red","Marker Color")
    green = cv2.getTrackbarPos("Green","Marker Color")
    blue = cv2.getTrackbarPos("Blue","Marker Color")
    # print(red)
    # print(green)
    # print(blue)

    #Below code checks the color and creates a binary mask.
    #Shows white when it detects the color
    if(blue):
        lower_blue = np.array([64, 72, 49])
        upper_blue = np.array([153, 255, 255])
        mask0 = cv2.inRange(hsv, lower_blue, upper_blue)
        lower_blue = np.array([180, 255, 255])
        upper_blue = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    elif(red):
        lower_red = np.array([0, 90, 50])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red = np.array([170, 90, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
    elif(green):
        lower_green = np.array([50, 50, 50])
        upper_green = np.array([70, 255, 255])
        mask0 = cv2.inRange(hsv, lower_green, upper_green)
        mask1 = 0


    #Below codes create buttons for color
    frame = cv2.rectangle(frame, (40, 1), (140, 65),(122, 122, 122), -1)
    frame = cv2.rectangle(frame, (160, 1), (255, 65),colors[0], -1)
    frame = cv2.rectangle(frame, (275, 1), (370, 65),colors[1], -1)
    frame = cv2.rectangle(frame, (390, 1), (485, 65),colors[2], -1)
    frame = cv2.rectangle(frame, (505, 1), (600, 65),colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(150, 150, 150), 2, cv2.LINE_AA)


    #Applying erosion and dilation to the mask to make it bigger.
    Mask = mask0+mask1
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    #FInding the contours
    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(cnts)
    center=0

    if(len(cnts)>0):
        #Sorting the contours from higest to lowest and choosing the highest one
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        (x, y), radius=cv2.minEnclosingCircle(cnt)                  #Getting the center point and radius
        print(radius)
        cv2.circle(frame,(int(x),int(y)),int(radius),(0, 255, 255),2)               #Displays a circle around the center

    #Shows all the frames
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask", Mask)

    if cv2.waitKey(1) & 0xFF == ord("e"):                                   #Click e to end the program
        break