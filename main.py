# from . import A
import win32api
import win32con
import Tkinter as tk
from Tkinter import *
import datetime
import time
import threading
import pyautogui
from PIL import ImageTk, Image
import tkMessageBox as messagebox
import numpy
import mss
from key_control.dd import dd
import analisys as analisys

sct= mss.mss()
# The screen part to capture
region = {'top': 400, 'left': 998, 'width': 100, 'height': 30}
# Grab the data
rgb1 = numpy.array([1,1,0])
print rgb1
class getPicTask(threading.Thread):
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False


    def run(self, i):
        isFishing=False
        isSpace=False
        while (self._running):
            # print datetime.datetime.now()
            # im = pyautogui.screenshot(region=(0, 0, 200, 200))

            # print datetime.datetime.now()

            #print datetime.datetime.now()
            if analisys.BDOCompareFishingSpace():
                time.sleep(1)
                dd('space') 
                time.sleep(1)
                isSpace=True
                while isSpace and self._running:
                    sct_img = sct.grab(region)
                    im = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw',
                                        'BGRX')
                    #mss.tools.to_png(sct_img.rgb, sct_img.size, output='dummy.png')
                    img = ImageTk.PhotoImage(im)
                    img_panel.configure(image=img)
                    img_panel.image = img
                    
                    v_top=4
                    v_bottom=25
                    if isFishing==False:
                        for index in range(0, 92):
                            rt, gt, bt = im.getpixel((index, v_top))
                            rb, gb, bb = im.getpixel((index, v_bottom))
                            if rt==gt==bt==rb==gb==bb==222:
                                isFishing=True
                    else:
                        #print datetime.datetime.now()
                        #im.save("general.png")
                        #image.open("newone.png").convert("RGB").save("newone.png")
                        key_x = 95
                        key_x_limit = 96
                        diff=95
                        key_y = 7
                        key_y_limit = 22
                        isTouch = True
                        for index in range(key_y, key_y_limit):
                            r, g, b = im.getpixel((key_x-diff, index))
                            if r < 125 and g < 125 and b < 125:
                                isTouch = False

                        if isTouch:
                            #print datetime.datetime.now() 
                            dd('space') 
                            #print datetime.datetime.now()
                            print "catch"
                            isGame=False
                            while isFishing and self._running:
                                sct_img = sct.grab(region)
                                im = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw',
                                                    'BGRX')
                                for index in range(0, 92):
                                    rt, gt, bt = im.getpixel((index, v_top))
                                    rb, gb, bb = im.getpixel((index, v_bottom))
                                    if not(rt>=222 and gt>=222 and bt>=222 and rb>=222 and gb >=222 and bb>=222):
                                        isGame=True
                                        im.save("general.png")
                                        
                                if isGame:
                                    isFishing=False
                                    game_img=analisys.captureFishingGame()
                                    keyboardData=analisys.analisysKeyBoard(numpy.array(game_img))
                                    if len(keyboardData['sort_key'])>0:
                                        for key in keyboardData['sort_key']:
                                            collection=keyboardData['data']
                                            print collection[key]
                                            dd(collection[key])
                                            time.sleep(0.1)
                            print "catch end "
                            time.sleep(10)
                            isSpace=False
                            img = ImageTk.PhotoImage(im)
                            img_panel.configure(image=img)
                            img_panel.image = img
                            #pyautogui.keyDown('space')
                            #pyautogui.keyUp('space')
                            #pyautogui.press('space')
                        #96 110~119
                        #pyautogui.pixel(200, 200)
                        #if impx==(185,192,179):
                        #print 'this is a number: ', i, impx
            else:
                time.sleep(1)
            



window = tk.Tk()
window.title('for test')
window.geometry('300x400')
screenWidth, screenHeight = pyautogui.size()
#im = pyautogui.screenshot(region=(0, 0, 100, 100))
sct_img = sct.grab(region)
im=Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
var = tk.StringVar()
#pyautogui.alert(text='', title='', button='OK')
screen = tk.Label(
    window,
    text=screenWidth.__str__() + ',' + screenHeight.__str__(),
    bg='white',
    font=('Arial', 12),
    width=20,
    height=2)
#l = tk.Label(window, text='OMG! this is TK!', bg='green', font=('Arial', 12), width=15, height=2)
print im
img = ImageTk.PhotoImage(im)
img_panel = tk.Label(window, image=img)
#screen.pack()
img_panel.pack()

#color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x , y)

on_hit = False

thead_arr = []


def hit_me():
    on_hit = True
    getPic = getPicTask()
    thread = threading.Thread(target=getPic.run, args=(11, ))
    thread.start()
    thead_arr.append(getPic)
    currentMouseX, currentMouseY = pyautogui.position()
    fb_str = "%s %s" % (currentMouseX, currentMouseY)


def stop_me():
    for x in thead_arr:
        x.terminate()


def ColorDistance(rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2+rm,4,3-rm)*(rgb1-rgb2)**2)**0.5
    return d

frame=Frame(window)
frame.grid(row=2, column=0, columnspan=2)     
b = tk.Button(frame, text='hit me', command=hit_me).grid(row=0,column=0)
b = tk.Button(frame, text='stop me', command=stop_me).grid(row=0,column=1)

frame.pack()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        for x in thead_arr:
            x.terminate()
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
