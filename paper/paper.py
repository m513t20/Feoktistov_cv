import cv2
import numpy as np
from pathlib import Path
import os 


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

file=Path(__file__).parent

n = 0

image =cv2.imread(os.path.join(file,"out.png"))


# hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


# _,thresh=cv2.threshold(hsv[:,:,1],70,255,cv2.THRESH_BINARY)


cv2.imshow("Image", image)


key = cv2.waitKey()


cv2.destroyAllWindows()