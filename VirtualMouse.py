import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui as pg

cam = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

screenWidth, screenHeight = pg.size()  # görüntü boyutu
print(screenWidth, screenHeight)

frameR = 100

fingersId = [4, 8, 12, 16, 20]  # parmak ucu id leri
click = 1

while True:
    succes, image = cam.read()

    image = cv.flip(image, 1)

    height, width, c = image.shape

    imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    response = hands.process(imageRGB)

    cv.rectangle(image, (frameR, frameR), (width-frameR, height-frameR),
                 (255, 0, 0), 2)  # kutu

    if (response.multi_hand_landmarks):

        #göründüği yer
        tangan = response.multi_handedness[0].classification[0].label
        if tangan == "Right":  # sağ eli algıladığında çalışır
            lmlist = []

            for handLms in response.multi_hand_landmarks:
                for id, landmarks in enumerate(handLms.landmark):
                    cx, cy = int(landmarks.x*width), int(landmarks.y*height)
                    lmlist.append([id, cx, cy])


            fingers = []
            if lmlist[fingersId[0]][1] < lmlist[fingersId[0]-2][1]:  # baş parmak
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):  # işaret parmak - serçe parmağı
                if lmlist[fingersId[id]][2] < lmlist[fingersId[id]-3][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            """Fare hareketi """
            if fingers == [0, 1, 1, 0, 0]:
                # orta parmağa  mouse imleci
                cv.circle(image, (lmlist[12][1], lmlist[12]
                          [2]), 10, (0, 233, 255), cv.FILLED)

                # x ekseni
                X = np.interp(
                    lmlist[12][1], (frameR, width-frameR), (0, screenWidth))
                # y ekseni
                Y = np.interp(lmlist[12][2], (frameR, height -
                              frameR), (0, screenHeight))

                # orta parmak ile işaret parmağı arası x uzaklığı
                length = abs(lmlist[8][1] - lmlist[12][1])

                pg.moveTo(X, Y, duration=0.3)

                # tıklama
                if (lmlist[8][2] > lmlist[7][2]) and click > 0:
                    pg.click()
                    click = -1
                elif (lmlist[8][2] < lmlist[7][2]):
                    click = 1

                # sürükleme
                if length > 50:
                    pg.mouseDown(button = 'left')
                    pg.scroll(100)
                else:
                    pg.scroll(-100)
                    pg.mouseUp(button = 'left')

    cv.imshow("webcam", image)

    if cv.waitKey(20) & 0xFF == ord('d'):  # d ye bas ve çık
        break

cv.destroyAllWindows()
