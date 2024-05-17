import matplotlib.pyplot as plt
import pyautogui
import webbrowser
import time
import cv2 
import keyboard
import os
from pathlib import Path
from work_with_pictures import get_head
import numpy as np
import mss 

dir=Path(__file__).parent
file=os.path.join(dir,'trex_the_game.html')
start=cv2.imread(os.path.join(dir,"start_position.png"))
x=0
y=0


def copy_game():
    global file
    in_f="""<head> </head>
<body>
<iframe src="https://chromedino.com/" frameborder="0" scrolling="no" width="100%" height="100%" loading="lazy"></iframe>
<style type="text/css">iframe { position: absolute; width: 500px; height: 700px; z-index: 999; }</style>
</body>"""
    with open(file,'w') as game_cpy:
        game_cpy.write(in_f)

def open_game():
    global file
    webbrowser.open(file)

def start_game():
    global x,y
    global start
    out=False
    while not out:
        try:
            tmp=pyautogui.locateOnScreen(start)
            x = tmp[0]
            y = tmp[1]
            out=True
        except:
            pass
    
    pyautogui.leftClick(x,y)
    pyautogui.press('space')

def down():
    pyautogui.press('down')


def short_jump():
    with pyautogui.hold('space'):
        time.sleep(0.14)
    down()

    

def long_jump(jump_time=0):
    pyautogui.press('space')
    time.sleep(jump_time)
    down()


def full_jump():
    pyautogui.press('space')

open_game()
time.sleep(7)
start_game()
#координаты скринов
line=500
interval=30
x=int(x)
y=int(y)

#интерва 60

#позиции для окон
startx=55
finishx=117

startx_timer=210
finishx_timer=275

windowx=50
windowy=[30,20,20]


# cv2.namedWindow("deb",cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow("head",cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow("ground",cv2.WINDOW_GUI_NORMAL)
# cv2.namedWindow("ground_deb",cv2.WINDOW_GUI_NORMAL)

    
kernel = np.ones((5,5),np.uint8)
#3451
print(x,y)
start_time=0
jump_time=0
jump_start_time=0
max_jump_time=0
duck_start_time=0
is_not_bird=0
is_grounded=True

past_max=False
step=40
begining_time=time.time()

mod=0
level=1
while True:
    #39
    
    
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": line, "height": 30}
        sct_img = sct.grab(monitor)
        bin_image=np.array(sct_img)
        
        # mss.tools.to_png(sct_img.rgb, sct_img.size, output=dir/"head.png")
        
        monitor = {"top": y+interval, "left": x, "width": line, "height": 20}
        sct_img = sct.grab(monitor)
        leggs_bin=np.array(sct_img)

        # mss.tools.to_png(sct_img.rgb, sct_img.size, output=dir/"ground.png")

        # monitor = {"top": y-interval, "left": x, "width": line, "height": 30}
        # sct_img = sct.grab(monitor)

        # mss.tools.to_png(sct_img.rgb, sct_img.size, output=dir/"sky.png")

    not_bin_image=cv2.bitwise_not(bin_image)
    not_bin_legs=cv2.bitwise_not(leggs_bin)

    _,head=cv2.threshold(not_bin_image,50,255,cv2.THRESH_BINARY)
    _,ground=cv2.threshold(not_bin_legs,50,255,cv2.THRESH_BINARY)

    head=cv2.dilate(head,kernel,iterations=1)
    ground=cv2.erode(ground,kernel,iterations=1)
    ground=cv2.dilate(ground,kernel,iterations=1)

    cact_norm=np.any(head[:,startx:finishx]) 


    ground_timer=np.any(ground[:,startx_timer:finishx_timer]) 
    cact_timer=np.any(head[:,startx_timer:finishx_timer]) 

    cur_time=time.time()
    #ускорение
    if step<200 and cur_time-begining_time>=step:
        print(f'level_up! {level}')
        level+=1
        step+=40
        finishx+=5
        finishx_timer+=5
        mod+=0.009
    #он пока не собирается останавливаться
    #начало измерения скорости
    if (cact_timer ) and start_time ==0:

        start_time=cur_time
    #проверка на птицу
    if start_time!=0 and ground_timer:
        is_not_bird+=1
    #скорость в секундах
    if not(cact_timer ) and start_time >0:

        jump_time=cur_time-start_time
        #print(jump_time)
    
        start_time=0
    #прыжок или подкат
    if cact_norm and is_grounded:
        if is_not_bird>0:
            keyboard.press('space')
            jump_start_time=cur_time
            is_grounded=False
            is_not_bird=0
        else:
            keyboard.press('down')
            duck_start_time=cur_time

    #встать
    if duck_start_time!=0 and cur_time-duck_start_time>jump_time:
        keyboard.release("down")
        duck_start_time=0

            
    #упасть
    if  not (is_grounded) and cur_time-jump_start_time>=jump_time-mod:

        keyboard.release('space')

        past_max=True
        
        jump_time=100000
        keyboard.press('down')
        max_jump_time=cur_time
    #перестать падать
    if max_jump_time!=0 and cur_time-max_jump_time>=0.08:
        is_grounded=True
        keyboard.release('down')
        max_jump_time=0
        
        


        

    # cv2.rectangle(bin_image,(startx,0),(finishx,30),(0,0,255),4)
    # cv2.rectangle(bin_image,(startx_timer,0),(finishx_timer,30),(0,255,0),4)
    # cv2.rectangle(leggs_bin,(startx,0),(finishx,30),(0,0,255),4)
    # cv2.rectangle(leggs_bin,(startx_timer,0),(finishx_timer,30),(0,255,0),4)

    # cv2.imshow("head",head)
    # cv2.imshow("deb",bin_image)
    # cv2.imshow('ground',ground)
    # cv2.imshow('ground_deb',leggs_bin)

