import matplotlib.pyplot as plt
import pyautogui
import webbrowser
import time
import cv2 
import keyboard
import os
from pathlib import Path
from skimage.measure import label
import numpy as np



dir=Path(__file__).parent
def get_images():
    global dir
    cv2.namedWindow("sky",cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow("head",cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow("ground",cv2.WINDOW_GUI_NORMAL)

    sky=cv2.imread(os.path.join(dir,"sky.png"))
    head=cv2.imread(os.path.join(dir,"head.png"))
    ground=cv2.imread(os.path.join(dir,"ground.png"))
    sky_g=cv2.cvtColor(sky,cv2.COLOR_BGR2GRAY)
    head_g=cv2.cvtColor(head,cv2.COLOR_BGR2GRAY)
    ground_g=cv2.cvtColor(ground,cv2.COLOR_BGR2GRAY)

    sky_g=cv2.bitwise_not(sky_g)
    thr1=cv2.threshold(sky_g,50,255,cv2.THRESH_BINARY)[1]
    head_g=cv2.bitwise_not(head_g)
    thr2=cv2.threshold(head_g,50,255,cv2.THRESH_BINARY)[1]
    ground_g=cv2.bitwise_not(ground_g)
    thr3=cv2.threshold(ground_g,50,255,cv2.THRESH_BINARY)[1]

    
    kernel = np.ones((5,5),np.uint8)
    thr3=cv2.erode(thr3,kernel,iterations=1)
    return[thr1,thr2,thr3]




def get_images_show():
    global dir
    cv2.namedWindow("sky",cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow("head",cv2.WINDOW_GUI_NORMAL)
    cv2.namedWindow("ground",cv2.WINDOW_GUI_NORMAL)

    sky=cv2.imread(os.path.join(dir,"sky.png"))
    head=cv2.imread(os.path.join(dir,"head.png"))
    ground=cv2.imread(os.path.join(dir,"ground.png"))
    sky_g=cv2.cvtColor(sky,cv2.COLOR_BGR2GRAY)
    head_g=cv2.cvtColor(head,cv2.COLOR_BGR2GRAY)
    ground_g=cv2.cvtColor(ground,cv2.COLOR_BGR2GRAY)

    sky_g=cv2.bitwise_not(sky_g)
    thr1=cv2.threshold(sky_g,50,255,cv2.THRESH_BINARY)[1]
    head_g=cv2.bitwise_not(head_g)
    thr2=cv2.threshold(head_g,50,255,cv2.THRESH_BINARY)[1]
    ground_g=cv2.bitwise_not(ground_g)
    thr3=cv2.threshold(ground_g,50,255,cv2.THRESH_BINARY)[1]

    
    kernel = np.ones((5,5),np.uint8)
    thr3=cv2.erode(thr3,kernel,iterations=1)



    cnts,hierarchy=cv2.findContours(thr1,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for ind,cnt in enumerate(cnts):
        cv2.drawContours(sky,cnts,ind,(0,0,255),1)

    cnts,hierarchy=cv2.findContours(thr2,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for ind,cnt in enumerate(cnts):
        cv2.drawContours(head,cnts,ind,(0,0,255),1)

    cnts,hierarchy=cv2.findContours(thr3,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for ind,cnt in enumerate(cnts):
        cv2.drawContours(ground,cnts,ind,(0,0,255),1)

    

    cv2.imshow('sky',sky)
    cv2.imshow('head',head)
    cv2.imshow('ground',ground)


    key=cv2.waitKey()
    cv2.destroyAllWindows()
