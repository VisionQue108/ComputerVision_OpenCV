
import cv2
import numpy as np
#These lines of code set the display window params
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)



def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 146, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 101, 255, empty)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)



def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):
    """
    cv2.RETR_EXTERNAL function is a retrival method that returns only the outermost contours
    cv2.CHAIN_APPROX_NONE function collects all the contour points .the NONE part means no points get compressed ,
    which if replaced by SIMPLE compresses the contour points and reduces the size of data collected
    """
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #(255,0,0) is the color and 3 is the line width


    for cnt in contours:
        #Gives us the area of the contours
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos('Area', 'Parameters')

        if area > areaMin:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            #print(area)
            #In order to find the corner points we first have to find the length of the contours
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            pts = len(approx)

            if pts == 3:

                #Drawing Bounding rectangular box
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(imgContour, 'Triangle' , (x + w + 20, y+20), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (0, 255, 0), 2)
                cv2.putText(imgContour, 'Area:' + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX,
                            0.7, (0, 255, 0), 2)

                print(x,y,w,h)




while True:

    #Assigns variable img to the data read on each frame which is being provided by cap
    success, img = cap.read()

    imgContour = img.copy()

    #Converts frame to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #7x7 Gaussian Filter on img
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)

    #Applying Canny function for edge detection
    threshold1 = cv2.getTrackbarPos('Threshold1', 'Parameters')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Parameters')
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))

    #Dilates the image(i.e makes the edges thicker)
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)

    #To Represent the detection process in layers
    """
    #Stacks the images
    imgStack = stackImages(0.8, ([imgCanny, imgGray, img], [imgContour, imgDil, imgContour]))
    """


    #Displays the each frame from img in a window named Result
    cv2.imshow("Result", imgContour)

    #Waits until the button q is pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break