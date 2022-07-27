import time

import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
pTime=0
cTime=0
while True:
    success, img = cap.read()
    #hands metodu görüntüyü rgb olarak işlediği için kameradan gelen görüntü rgb formatına dönüştürülüyor
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    #her bir el için eklemler noktalandı ve aralarındaki bağlantı belirtildi
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                #elimizin hareketlerini x ve y kordinatlarında gösteriyoruz
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                if id==4:
                    cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
                print(id,cx,cy)


                #print(id,lm)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
    #fps counter ekliyorum
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,30),cv2.FONT_HERSHEY_PLAIN,2,(144,215,0),2)

    cv2.imshow('img', img)
    cv2.waitKey(1)
