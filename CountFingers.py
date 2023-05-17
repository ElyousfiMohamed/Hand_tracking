import cv2
import time
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
preTime = 0
curTime = 0

detector = htm.HandTrackingModule()

while True:
    success, img = cap.read()
    fingers_count = 0

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False, handNo=0)

    if len(lmList) != 0:
        x5, y5 = lmList[5][1], lmList[5][2]
        x4, y4 = lmList[4][1], lmList[4][2]

        x6, y6 = lmList[6][1], lmList[6][2]
        x7, y7 = lmList[7][1], lmList[7][2]

        x10, y10 = lmList[10][1], lmList[10][2]
        x11, y11 = lmList[11][1], lmList[11][2]

        x14, y14 = lmList[14][1], lmList[14][2]
        x15, y15 = lmList[15][1], lmList[15][2]

        x18, y18 = lmList[18][1], lmList[18][2]
        x19, y19 = lmList[19][1], lmList[19][2]

        if y6 > y7:
            fingers_count += 1
        if y10 > y11:
            fingers_count += 1
        if y14 > y15:
            fingers_count += 1
        if y18 > y19:
            fingers_count += 1
        if y4 < y5:
            fingers_count += 1

        cv2.putText(img, str(fingers_count), (50, 400), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

    curTime = time.time()
    fps = 1 / (curTime - preTime)
    preTime = curTime

    cv2.putText(img, f'FPS:{str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
