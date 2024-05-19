import cv2
import numpy as np
from pathlib import Path
import os 


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)


lower=0
upper=73


file=Path(__file__).parent
text=str(input("enter your text: \n"))

n = 0
while True:

    image =cv2.imread(os.path.join(file,"out.png"))
    warped=image.copy()

    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


    _,thresh=cv2.threshold(hsv[:,:,1],70,255,cv2.THRESH_BINARY)

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(7,7),0)




    #0-73
    cany=cv2.Canny(gray,lower,upper)
    cnts,_=cv2.findContours(cany,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    rect=cv2.minAreaRect(cnts[0])

    box=cv2.boxPoints(rect)


    straight_pts=np.float32([[0,rect[1][1]],[rect[1][0],rect[1][1]],[0,0],[rect[1][0],0]])
    original_pts=np.float32([box[0],box[3],box[1],box[2]]) 


    to_straight=cv2.getPerspectiveTransform(original_pts,straight_pts)
    back_to_paper=cv2.getPerspectiveTransform(straight_pts,original_pts)
    warped=cv2.warpPerspective(image,to_straight,(int(rect[1][0]),int(rect[1][1])))
    cv2.putText(warped,text,(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0))
    warped=cv2.warpPerspective(warped,back_to_paper,(640,480))

    pos=np.where(warped>0)
    image[pos]=warped[pos]


    cv2.imshow("Image", image)

    key = cv2.waitKey()
    if key==ord('q'):
        break


cv2.destroyAllWindows()