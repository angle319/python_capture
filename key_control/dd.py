#!/usr/bin/python
#coding:utf-8
from ctypes import *

import time

# 註冊DD DLL，64位python用64位，32位用32位，具體看DD說明文件。
# 測試用免安裝版。
# 用哪個就調用哪個的dll文件。 
dll = windll.LoadLibrary('..\\dll\\DDHID32.dll')
dll.DD_btn(0)
# DD虛擬碼，可以用DD內置函數轉換。
vk = {'5': 205, 'c': 503, 'n': 506, 'z': 501, '3': 203, '1': 201, 'd': 403, '0': 210 , 'l': 409, '8': 208, 'w': 302,
'u': 307, '4': 204, 'e': 303, '[': 311, 'f': 404, 'y': 306, 'x': 502, 'g': 405, 'v': 504, 'r': 304, 'i': 308,
'a': 401, 'm': 507, 'h': 406, '.': 509, ',': 508, ']': 312, '/': 510, '6': 206, '2': 202, 'b': 505, 'k': 408,
'7': 207, 'q': 301, "'": 411, '\\': 313, 'j': 407, '`': 200, '9': 209, 'p': 310, 'o': 309, 't': 305, '-': 211,
'=': 212, 's': 402, ';': 410,'space':603,'win':601,"enter":313,"quest":510}
# 需要組合shift的按鍵。
vk2 = {'"': "'", '#': '3', ')': '0', '^': '6', ' ': '/', '>': '.' , '<': ',', '+': '=', '*': '8', '&': '7', '{': '[', '_': '-',
'|': '\\', '~': '`', ':': ';', '$': '4', '}': ']', '%': '5', ' @': '2', '!': '1', '(': '9'}

def down_up(code):
    # 進行一組按鍵。
    dll.DD_key(vk[code], 1) 
    dll.DD_key(vk[code], 2)

def dd(key):
    # 500是shift鍵碼。
    if key.isupper():
        # 如果是一個大寫的玩意。

        # 按下抬起。
        dll.DD_key(500, 1)
        down_up(key.lower())
        dll.DD_key(500, 2)

    elif key in '~!@#$%^&*()_+{}|:"<> ':
        # 如果是需要這樣按鍵的玩意。
        dll.DD_key(500, 1)
        down_up(vk2[key])
        dll.DD_key(500, 2)
    else:
        down_up(key)
        
def ddClick(x,y):
    #double screen need divided by two 
    dll.DD_mov(x/2,y)
    time.sleep(0.1)
    dll.DD_btn(1)
    time.sleep(0.1)
    dll.DD_btn(2)
    
time.sleep(0.5)
down_up('win')