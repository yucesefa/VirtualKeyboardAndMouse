import cv2 as cv
import mediapipe as mp
import pyautogui as pg

cam = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()

clk = 1
size = 100/100
keys = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?']]


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        x = int((j*60*size) + 25)
        y = int((i*60*size) + 60)
        h = int(x + 50*size)
        w = int(y + 50*size)
        buttonList.append([x, y, h, w, key])


def S_keys():
    def xs(i): return int((i*60*size) + 25)
    def ys(y): return int((y*60*size) + 60)
    def hws(hw): return int(hw + 50*size)
    buttonList.append([xs(0), ys(len(keys)), hws(
        xs(3)), hws(ys(len(keys))), 'backspace'])
    buttonList.append([xs(4), ys(len(keys)), hws(
        xs(6)), hws(ys(len(keys))), 'capslock'])
    buttonList.append([xs(7), ys(len(keys)), hws(
        xs(9)), hws(ys(len(keys))), 'enter'])
    buttonList.append([xs(1), ys(len(keys)+1), hws(xs(8)),
                      hws(ys(len(keys)+1)), ' '])


S_keys()

"""klavye olusturma"""


def drawKey(img, buttonList):
    for x, y, h, w, key in buttonList:
        cv.rectangle(img, (x, y), (h, w), (0, 0, 255), 2)
        cv.putText(img, key, (x+12, y+29),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)


while True:
    succes, img = cam.read()
    img = cv.flip(img, 1)

    h, w, c = img.shape

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB) # renk uzayını değiştime
    result = hands.process(imgRGB)
    if (result.multi_hand_landmarks): # birden fazla el yer işareti var mı
        lmlist = []
        for handsLms in result.multi_hand_landmarks:
            for id, landmarks in enumerate(handsLms.landmark):
                x, y = int(landmarks.x * w), int(landmarks.y * h)
                lmlist.append([id, x, y])
                # her el üzerinde yinelenir first for
                #second for her bir yer işaretinin x ve y koordinatları oluşturulur
                #el takibi gerçekleşir görüntü rgb formata dönüştürülür el izleme modülü ile
                # işlemler ve tespit edilen her el için konumlar belirlenir ve bir listede tutulur

        X = lmlist[12][1]
        Y = lmlist[12][2]
        cv.circle(img, (X, Y), 9, (0, 255, 255), cv.FILLED) # parmak ucu yuvarlak

        if (lmlist[8][2] > lmlist[7][2]) and ((clk > 0)):
            cv.circle(img, (X, Y), 9, (0, 255, 0), cv.FILLED)
            for x, y, h, w, keys in buttonList:
                if x < X < h and y < Y < w:
                    pg.press(keys)
            clk = -1 #birden fazla tuşa basılmaması için klik ibr kez kaydedilir

        elif (lmlist[8][2] < lmlist[7][2]):
            clk = 1 # işlemin algılanabileceğini temsil eder

            #el harekeinin klik hereketi algıladıgında el pozisyonunun bir düğmeye karşılık
            #gelip gelmediğine bakılıp işleme dökülür

    drawKey(img, buttonList)

    cv.imshow("frame", img)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cv.destroyAllWindows()
