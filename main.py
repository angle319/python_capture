import Tkinter as tk
import datetime
import time
import threading
import pyautogui
from PIL import ImageTk, Image
import tkMessageBox as messagebox
import numpy
import mss
sct= mss.mss()
    # The screen part to capture
region = {'top': 0, 'left': 1920, 'width': 200, 'height': 200}

    # Grab the data
rgb1 = numpy.array([1,1,0])
print rgb1
class getPicTask(threading.Thread):
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, i):
        while (self._running):
            # print datetime.datetime.now()
            # im = pyautogui.screenshot(region=(0, 0, 200, 200))

            # print datetime.datetime.now()
            
            #print datetime.datetime.now()
            sct_img = sct.grab(region)
            im=Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            #mss.tools.to_png(sct_img.rgb, sct_img.size, output='dummy.png')
            img = ImageTk.PhotoImage(im)
            img_panel.configure(image=img)
            img_panel.image = img
            #print datetime.datetime.now()
            #im.save("general.png")
            #image.open("newone.png").convert("RGB").save("newone.png")
            
            impx = im.getpixel((199, 199))
            #pyautogui.pixel(200, 200)
            #if impx==(185,192,179):
            print 'this is a number: ', i, impx
            #time.sleep(1)


window = tk.Tk()
window.title('for test')
window.geometry('300x400')
screenWidth, screenHeight = pyautogui.size()
#im = pyautogui.screenshot(region=(0, 0, 100, 100))
sct_img = sct.grab(region)
im=Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
var = tk.StringVar()
#pyautogui.alert(text='', title='', button='OK')
l = tk.Label(
    window,
    textvariable=var,
    bg='green',
    font=('Arial', 12),
    width=15,
    height=2)
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
screen.pack()
l.pack()
img_panel.pack()

#color = win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x , y)

on_hit = False

thead_arr = []


def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        getPic = getPicTask()
        thread = threading.Thread(target=getPic.run, args=(11, ))
        thread.start()
        thead_arr.append(getPic)
        currentMouseX, currentMouseY = pyautogui.position()
        fb_str = "%s %s" % (currentMouseX, currentMouseY)
        var.set(fb_str)
    else:
        on_hit = False
        var.set('')


def stop_me():
    for x in thead_arr:
        x.terminate()


def ColorDistance(rgb1,rgb2):
    '''d = {} distance between two colors(3)'''
    rm = 0.5*(rgb1[0]+rgb2[0])
    d = sum((2+rm,4,3-rm)*(rgb1-rgb2)**2)**0.5
    return d

b = tk.Button(window, text='hit me', width=15, height=2, command=hit_me)
b.pack()
b = tk.Button(window, text='stop me', width=15, height=2, command=stop_me)
b.pack()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        for x in thead_arr:
            x.terminate()
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
