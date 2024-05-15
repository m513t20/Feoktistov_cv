import matplotlib.pyplot as plt
import pyautogui
import webbrowser
import time
import cv2 
import keyboard
import os
from pathlib import Path
from skimage.measure import label



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
    tmp=pyautogui.locateOnScreen(start)
    x = tmp[0]
    y = tmp[1]
    
    pyautogui.leftClick(x,y)
    pyautogui.press('space')

def down():
    pyautogui.press('down')


def short_jump():
    with pyautogui.hold('space'):
        time.sleep(0.14)
    down()

    

def long_jump():
    with pyautogui.hold('space'):
        time.sleep(0.19)
    down()


def full_jump():
    pyautogui.press('space')

open_game()
time.sleep(7)
start_game()

line=500
interval=30
x=int(x)
y=int(y)


# pyautogui.screenshot(dir/"sky1.png",(x,y-interval,line,40))
# pyautogui.screenshot(dir/"head1.png",(x,y,line,20))
# pyautogui.screenshot(dir/'ground1.png',(x,y+interval,line,40))


cv2.namedWindow("sky",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("head",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("ground",cv2.WINDOW_GUI_NORMAL)

while True:
    #39
    pyautogui.screenshot(dir/"sky.png",(x,y-interval,line,40))
    sky=cv2.imread(os.path.join(dir,"sky.png"))
    sky_g=cv2.cvtColor(sky,cv2.COLOR_BGR2GRAY)
    sky_g=cv2.bitwise_not(sky_g)
    pyautogui.screenshot(dir/"head.png",(x,y,line,20))
    head=cv2.imread(os.path.join(dir,"head.png"))
    head_g=cv2.cvtColor(head,cv2.COLOR_BGR2GRAY)
    pyautogui.screenshot(dir/'ground.png',(x,y+interval,line+20,40))
    ground=cv2.imread(os.path.join(dir,"ground.png"))
    ground_g=cv2.cvtColor(ground,cv2.COLOR_BGR2GRAY)


    labeled=label(sky_g)
    plt.imshow(sky_g)
    plt.show()

    cv2.imshow('sky',sky_g)
    cv2.imshow('head',head_g)
    cv2.imshow('ground',ground_g)
    

    key=cv2.waitKey(1)
    if key==ord('q'):
        break