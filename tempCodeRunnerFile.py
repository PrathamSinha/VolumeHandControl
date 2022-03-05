import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin,volMax = volume.GetVolumeRange()[:2]
while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand-landmarks:
        for handlandmark in results.multi_hand_landmarks:
            h,w,_ = img.shape
            cx,cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id,cx,cy])
        mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

    # if lmList != []:
    #     x1,y1 = lmlist[4][1],lmList[4][2]
    #     x2,y2 = lmList[8][1],lmList[8][2]