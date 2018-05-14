
import numpy
import mss
import imutils
import cv2
sct=mss.mss()
def BDOCompareFishingSpace():
    region = {'top': 227, 'left': 921, 'width': 73, 'height': 27}
    sct_img = sct.grab(region)
    timage = cv2.imread('img\space_analysis.jpg')
    tgray=cv2.cvtColor(timage, cv2.COLOR_BGR2GRAY)
    tthresh = cv2.threshold(tgray, 190, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(numpy.array(sct_img), cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
    return  compareImage(thresh,tthresh,0.85)

def compareImage(image,c_image,value):
    result=cv2.matchTemplate(image,c_image,cv2.TM_CCOEFF_NORMED)
    x,y= numpy.where( result >= value)
    return len(x) and len(y) 
def captureFishingGame():
    region = {'top': 355, 'left': 775, 'width': 371, 'height': 50}
    sct_img = sct.grab(region)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output='dummy.png')
    return sct_img
# region = {'top': 350, 'left': 756, 'width': 387, 'height': 69}
# sct_img = sct.grab(region)
# image=numpy.array(sct_img)
def findall(search, image, threshold=0.7):
    w, h = search.shape[::-1]
    method = cv2.TM_CCOEFF_NORMED
    # method = cv2.TM_CCORR_NORMED

    res = cv2.matchTemplate(image, search, method)

    points = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        if max_val > threshold:
            # floodfill the already found area
            sx, sy = top_left
            for x in range(sx-w/2, sx+w/2):
                for y in range(sy-h/2, sy+h/2):
                    try:
                        res[y][x] = numpy.float32(-10000) # -MAX
                    except IndexError: # ignore out of bounds
                        pass
            # _show_image(image_file, top_left, (w, h))
            middle_point = (top_left[0]+w/2, top_left[1]+h/2)
            points.append(middle_point)
        else:
            break
    return points

#def analisysKeyBoard():
image = cv2.imread("k3.png")
A_img = cv2.imread("img\A.png")
A_img = cv2.cvtColor(A_img, cv2.COLOR_RGB2GRAY)
S_img = cv2.imread("img\S.png")
S_img = cv2.cvtColor(S_img, cv2.COLOR_RGB2GRAY)
D_img = cv2.imread("img\D.png")
D_img = cv2.cvtColor(D_img, cv2.COLOR_RGB2GRAY)
W_img = cv2.imread("img\W.png")
W_img = cv2.cvtColor(W_img, cv2.COLOR_RGB2GRAY)
# gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
# thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]


# Threshold the HSV image to get only blue colors  
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  
lower_red = numpy.array([0, 25, 25])  
upper_red = numpy.array([255, 230, 255])  

mask = cv2.inRange(hsv, lower_red, upper_red) #lower20===>0,upper200==>0  

# threshimage = cv2.threshold(gray, 100, 240, cv2.THRESH_BINARY) [1]
# edgedimage = cv2.Canny(threshimage, 50, 150)

# w = A_img.shape[1]
# h = A_img.shape[0]
# result=cv2.matchTemplate(mask,A_img,cv2.TM_CCOEFF);
# threshold = 0.8
# loc = numpy.where(result >= threshold) 
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
# print bottom_right
# cv2.rectangle(mask,top_left, bottom_right, 255, 2)

positions_a = findall(A_img, mask, 0.5)
positions_s = findall(S_img, mask, 0.5)
positions_d = findall(D_img, mask, 0.5)
positions_w = findall(W_img, mask, 0.5)

element={}
def intoArray(collection,key):
    for x,y in collection:
        element[x]=key
intoArray(positions_a,'A')
intoArray(positions_s,'S')
intoArray(positions_d,'D')
intoArray(positions_w,'W')
ket_list=element.keys()
ket_list.sort()
print element
print ket_list
print {'sort_key':ket_list,'data':element }



# thresh = cv2.threshold(gray, 100, 120, cv2.THRESH_BINARY)[1]
cv2.imshow("Image", mask) 
#cv2.imwrite('perfect.png', mask)
cv2.waitKey(0)


#print BDOCompareFishingSpace()

#cv2.imshow("Image", thresh) 
#cv2.imwrite('space_analysis.png', thresh)
#cv2.waitKey(0)