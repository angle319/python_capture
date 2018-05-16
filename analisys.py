
import numpy
import mss
import imutils
import cv2
from PIL import Image
sct=mss.mss()
A_img = cv2.imread("img\A.png")
A_img = cv2.cvtColor(A_img, cv2.COLOR_RGB2GRAY)
S_img = cv2.imread("img\S.png")
S_img = cv2.cvtColor(S_img, cv2.COLOR_RGB2GRAY)
D_img = cv2.imread("img\D.png")
D_img = cv2.cvtColor(D_img, cv2.COLOR_RGB2GRAY)
W_img = cv2.imread("img\W.png")
W_img = cv2.cvtColor(W_img, cv2.COLOR_RGB2GRAY)

def compareImage(image,c_image,value):
    result=cv2.matchTemplate(image,c_image,cv2.TM_CCOEFF_NORMED)
    x,y= numpy.where( result >= value)
    return len(x) and len(y) 
def captureFishingGame():
    region = {'top': 348, 'left': 775, 'width': 371, 'height': 70}
    sct_img = sct.grab(region)
    #mss.tools.to_png(sct_img.rgb, sct_img.size, output='dummy.png')
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

def isKeyItem(image):
    gray = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2GRAY)
    key_img = cv2.imread("img\key.png")
    key_img = cv2.cvtColor(key_img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('key.png', key_img)
    position=findall(key_img, gray, 0.6)
    if len(position)>0:
        print "is key"
        return 1
    return 0
def isStoneItem(image):
    gray = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2GRAY)
    stone_img = cv2.imread("img\stone.png")
    stone_img = cv2.cvtColor(stone_img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('stone.png', stone_img)
    position=findall(stone_img, gray, 0.6)
    if len(position)>0:
        print "is stone"
        return 1
    return 0
def isColorPackage(image,_rgb):
    base_r,base_g,base_b=_rgb
    total=0
    im = Image.frombytes('RGB', image.size, image.bgra, 'raw','BGRX')
    for y in range(13):#image.height
        for x in range(image.width):
            r,g,b =  im.getpixel((x, y))
            if abs(r-base_r)<20 and abs(g-base_g)<20 and abs(b-base_b)<20:
                total+=1
            if total>3:
                print "is color "
                return 1
        total=0
    return 0
    
def isCapturePackage():
    region = {'top': 590, 'left': 1534, 'width': 193, 'height': 150}
    sct_img = sct.grab(region)
    if (isColorPackage(sct_img,(188,157,85))) or (isColorPackage(sct_img,(70,148,188))) or (isKeyItem(sct_img)) or (isStoneItem(sct_img)):
        return 1
    return 0

def BDOCompareFishingSpace():
    #region = {'top': 227, 'left': 921, 'width': 73, 'height': 27}
    region = {'top': 227, 'left': 921, 'width': 73, 'height': 80}
    sct_img = sct.grab(region)
    #mss.tools.to_png(sct_img.rgb, sct_img.size, output="log.png")
    timage = cv2.imread('img\space_analysis.jpg')
    tgray=cv2.cvtColor(timage, cv2.COLOR_BGR2GRAY)
    tthresh = cv2.threshold(tgray, 190, 255, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(numpy.array(sct_img), cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)[1]
    position=findall(thresh, tthresh, 0.6)
    if len(position)>0:
        return 1
    return 0
    #return  compareImage(thresh,tthresh,0.85)

def analisysHLSKeyBoard(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  
    lower_red = numpy.array([0, 25, 25])  
    upper_red = numpy.array([255, 230, 255])  
    mask = cv2.inRange(hsv, lower_red, upper_red)
    positions_a = findall(A_img, mask, 0.6)
    positions_s = findall(S_img, mask, 0.6)
    positions_d = findall(D_img, mask, 0.6)
    positions_w = findall(W_img, mask, 0.6)

    element={}
    def intoArray(collection,key):
        for x,y in collection:
            element[x]=key
    intoArray(positions_a,'a')
    intoArray(positions_s,'s')
    intoArray(positions_d,'d')
    intoArray(positions_w,'w')
    ket_list=element.keys()
    ket_list.sort()
    return {'sort_key':ket_list,'data':element }


def analisysHSVKeyBoard(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  
    lower_red = numpy.array([0, 0, 100])  
    upper_red = numpy.array([0, 50, 240]) 
    mask = cv2.inRange(hsv, lower_red, upper_red)
    positions_a = findall(A_img, mask, 0.55)
    positions_s = findall(S_img, mask, 0.55)
    positions_d = findall(D_img, mask, 0.55)
    positions_w = findall(W_img, mask, 0.55)

    element={}
    def intoArray(collection,key):
        for x,y in collection:
            element[x]=key
    intoArray(positions_a,'a')
    intoArray(positions_s,'s')
    intoArray(positions_d,'d')
    intoArray(positions_w,'w')
    ket_list=element.keys()
    ket_list.sort()
    return {'sort_key':ket_list,'data':element }

