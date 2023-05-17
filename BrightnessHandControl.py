import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
import screen_brightness_control as sbc

camWidth, camHeight = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)
preTime = 0
curTime = 0

detector = htm.HandTrackingModule()

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False, handNo=0)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        brightness_level = np.interp(length, [20, 170], [0, 100])
        sbc.set_brightness(brightness_level)

        brightness_bar = np.interp(length, [20, 170], [400, 150])
        brightness_per = np.interp(length, [20, 170], [0, 100])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
        cv2.rectangle(img, (50, int(brightness_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'{int(brightness_per)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    curTime = time.time()
    fps = 1 / (curTime - preTime)
    preTime = curTime

    cv2.putText(img, f'FPS:{str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
