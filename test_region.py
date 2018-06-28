
import numpy
import mss
import imutils
import cv2
sct=mss.mss()

def BDOCompareFishingSpace():
    region = {'top': 476, 'left': 863, 'width': 192, 'height': 43}
    sct_img = sct.grab(region)
    #timage = cv2.imread('img\space_analysis.jpg')
    #tgray=cv2.cvtColor(timage, cv2.COLOR_BGR2GRAY)
    #tthresh = cv2.threshold(tgray, 190, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(numpy.array(sct_img), cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Image", thresh) 
    cv2.waitKey(0)

    #return  compareImage(thresh,tthresh,0.85)
def BDOComparePackageSpace(): 
    region = {'top': 590, 'left': 1534, 'width': 193, 'height': 150}
    #region = {'top': 300, 'left': 1500, 'width': 400, 'height': 500}
    sct_img = sct.grab(region)
    #timage = cv2.imread('img\space_analysis.jpg')
    #tgray=cv2.cvtColor(timage, cv2.COLOR_BGR2GRAY)
    #tthresh = cv2.threshold(tgray, 190, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(numpy.array(sct_img), cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", numpy.array(gray)) 
    cv2.waitKey(0)

    #return  compareImage(thresh,tthresh,0.85)




BDOComparePackageSpace()
