import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pyttsx3

# img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('myDataFile.text') as f:
    myDataList = f.read().splitlines()
    engine=pyttsx3.init()
    engine.say("Please show your QR code")
    engine.runAndWait()

while True:

    success, img = cap.read()
    for barcode in decode(img):
        
        myData = barcode.data.decode('utf-8')
        
        if myData in myDataList:
            myOutput = 'Authorized'
            myColor = (0, 255, 0)
            engine.say("Welcome Back Authorized User!!")
            engine.runAndWait()
            exit()
        
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)
            engine.say("Unauthorized User!!!!!1")
            engine.runAndWait()

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Verification', img)
    cv2.waitKey(1)
