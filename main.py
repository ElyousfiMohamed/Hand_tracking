import cv2
import time
import HandTrackingModule as htm


def main():
    cap = cv2.VideoCapture(0)
    preTime = 0
    curTime = 0
    detector = htm.HandTrackingModule()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False, handNo=0)

        print(lmList)

        curTime = time.time()
        fps = 1 / (curTime - preTime)
        preTime = curTime

        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
