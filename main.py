import numpy as np
import cv2

# Code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255

# cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
#Array which holds colors
colors = [(255, 0, 0), (0, 255, 0),
          (0, 0, 255), (0, 255, 255)]

cap = cv2.VideoCapture(0)


while(True):
    ret, frame = cap.read()                                         #Video frame

    frame = cv2.rectangle(frame, (40, 1), (140, 65),
                          (122, 122, 122), -1)
    frame = cv2.rectangle(frame, (160, 1), (255, 65),
                          colors[0], -1)
    frame = cv2.rectangle(frame, (275, 1), (370, 65),
                          colors[1], -1)
    frame = cv2.rectangle(frame, (390, 1), (485, 65),
                          colors[2], -1)
    frame = cv2.rectangle(frame, (505, 1), (600, 65),
                          colors[3], -1)

    cv2.putText(frame, "CLEAR ALL", (49, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "BLUE", (185, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "GREEN", (298, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "RED", (420, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(frame, "YELLOW", (520, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (150, 150, 150), 2, cv2.LINE_AA)

    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) & 0xFF == ord("e"):                                   #Click e to end the program
        break