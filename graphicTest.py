
# import the necessary packages
import argparse
import imutils
import cv2
import mss
# construct the argument parse and parse the arguments

sct=mss.mss()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to the input image")
args = vars(ap.parse_args())
 
# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (1,1), 0)
thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
canny = cv2.Canny(thresh, 50, 150)  
# find contours in the thresholded image
# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
# 	cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# for c in cnts:
# 	# compute the center of the contour
# 	M = cv2.moments(c)
# 	cX = int(M["m10"] / M["m00"])
# 	cY = int(M["m01"] / M["m00"])
 
# 	# draw the contour and center of the shape on the image
# 	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
# 	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
# 	cv2.putText(image, "center", (cX - 20, cY - 20),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
# 	# show the image
# 	cv2.imshow("Image", thresh)
# 	cv2.waitKey(0)

cv2.imwrite('space_analysis.jpg', thresh)
cv2.imshow("Image", thresh)
cv2.waitKey(0)