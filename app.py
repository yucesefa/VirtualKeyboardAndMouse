import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
from keys import *
from pynput.keyboard import Controller
import time
from handTracker import *


def getPos(event, x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        # print(x,y)
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
        #     print(x,y)
        mouseX, mouseY = x, y


def calculateDistance(pt1, pt2):
    return int(((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5)


w, h = 80, 60
startX, startY = 40, 200
keys = []
letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
for i, l in enumerate(letters):
    if i < 10:
        keys.append(Key(startX + i * w + i * 5, startY, w, h, l))
    elif i < 19:
        keys.append(Key(startX + (i - 10) * w +
                    i * 5, startY + h + 5, w, h, l))
    else:
        keys.append(Key(startX + (i - 19) * w + i *
                    5, startY + 2 * h + 10, w, h, l))

keys.append(Key(startX + 25, startY + 3 * h + 15, 5 * w, h, "Space"))
keys.append(Key(startX + 8 * w + 50, startY + 2 * h + 10, w, h, "clr"))
keys.append(Key(startX + 5 * w + 30, startY + 3 * h + 15, 5 * w, h, "<--"))

textBox = Key(startX, startY - h - 5, 10 * w + 9 * 5, h, '')


detector = HandDetector(detectionCon=0.8, maxHands=2)
tracker = HandTracker(detectionCon=0.8)

cap = cv2.VideoCapture(0)
cap.set(3, 2120)
cap.set(4, 1080)
ptime = 0


clickedX, clickedY = 0, 0
mousX, mousY = 0, 0

show = False
cv2.namedWindow('video')
count = 0
previousClick = 0

keyboard = Controller()

while True:

    if count > 0:
        count -= 1

    signTipX = 0
    signTipY = 0

    thumbTipX = 0
    thumbTipY = 0

    lmList = tracker.getPosition(img, draw=False)
    if lmList:
        signTipX, signTipY = lmList[8][1], lmList[8][2]
        thumbTipX, thumbTipY = lmList[4][1], lmList[4][2]
        if calculateDistance((signTipX, signTipY), (thumbTipX, thumbTipY)) < 50:
            centerX = int((signTipX + thumbTipX) / 2)
            centerY = int((signTipY + thumbTipY) / 2)
            cv2.line((signTipX, signTipY),
                     (thumbTipX, thumbTipY), (0, 255, 0), 2)
            cv2.circle((centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = int(1 / (ctime - ptime))
    cv2.setMouseCallback('video', getPos)

    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            fingers2 = detector.fingersUp(hand2)

            p1 = lmList1[8][:2]
            p2 = lmList2[8][:2]
            print(p1)

            # Find Distance between two Landmarks. Could be same hand or different hands
            length, info, img = detector.findDistance(p1, p2, img)  # with draw
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
