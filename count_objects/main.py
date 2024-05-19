import cv2
import numpy as np
from skimage.measure import label,regionprops
import os 
from pathlib import Path






file=os.path.join(Path(__file__).parent,"out.jpeg")

n=0
cv2.namedWindow("Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Exmp",cv2.WINDOW_GUI_NORMAL)


while True:

    image=cv2.imread(file)
    key=cv2.waitKey(10)
    if key==ord('q'):
        break
    



    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


    ret,mask=cv2.threshold(hsv[:,:,1],70,255,cv2.THRESH_BINARY)


    result=cv2.bitwise_and(image,image,mask=mask)
    result=cv2.dilate(result,None,iterations=8)
    
    cnts,_=cv2.findContours(result,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    
    for index,cnt in enumerate(cnts):
        cv2.drawContours(result,cnts,index,(0,255,0),4)



    cv2.imshow("Exmp",result)

    bin_res=result.mean(2)
    bin_res[bin_res>0]=1
    grey=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    

    labeled=label(bin_res)


    cv2.putText(image,f"Image={n}, Cubes={labeled.max()}",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(127,255,255))
    cv2.putText(image,f"Image={n}, Cubes={labeled.max()}",(10,120),cv2.FONT_HERSHEY_SIMPLEX,0.7,(127,255,255))
    cv2.imshow("Image",image)



# cv2.imshow("Image",result)
# cv2.waitKey()

cv2.destroyAllWindows()