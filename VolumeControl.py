import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#kameramızın yükseklik ve genişliğini ayarlayalım
wCam,hCam=640,480


pTime=0
cTime=0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
print(volRange)
volume.SetMasterVolumeLevel(-20.0, None)
minVol=volRange[0]
maxVol=volRange[1]

while True:

    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    #lmList 4 değeri baş parmağın 8 değeri işaret parmağının ucunun x,y koordinatlarını yazdıracak
    if len(lmList)!=0:
        #print(lmList[4], lmList[8])

        #4 ve 8 numaralı eklemleri markladık
        x1,y1=lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),7,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2, y2), 7, (144, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 7, (144, 0, 0), cv2.FILLED)

        uzaklık=math.hypot(x2-x1,y2-y1)
        if uzaklık<30:
            cv2.circle(img, (cx, cy), 7, (255, 31, 129), cv2.FILLED)
        #print(int(uzaklık))

        #Hand range 200-30
        #Volume -96-0

        vol=np.interp(uzaklık,[30,200],[minVol,maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        #4 ve 8 nolu eklemler arası bir çizgi çekiyoruz
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

    # fps counter ekliyorum
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (144, 215, 0), 2)

    #görüntüleme
    cv2.imshow('img', img)
    cv2.waitKey(1)