import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

camWidth, camHeight = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeight)
preTime = 0
curTime = 0

detector = htm.HandTrackingModule()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False, handNo=0)

    if len(lmList) != 0:
        x2, y2 = lmList[4][1], lmList[4][2]
        x1, y1 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        vol = np.interp(length, [20, 190], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        vol_bar = np.interp(length, [20, 190], [400, 150])
        vol_per = np.interp(length, [20, 190], [0, 100])

        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f'{int(vol_per)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    curTime = time.time()
    fps = 1 / (curTime - preTime)
    preTime = curTime

    cv2.putText(img, f'FPS:{str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
