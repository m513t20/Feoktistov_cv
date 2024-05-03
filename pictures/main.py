import cv2 
import os
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import binary_closing,binary_erosion,binary_opening,binary_dilation
from pathlib import Path

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)

file_path=Path(__file__).parent
file_name="pictures.avi"
# saving_path=file_path/"images"
# saving_path.mkdir(exist_ok=True)

video = cv2.VideoCapture(os.path.join(file_path,file_name))
frames=0


while video.isOpened():
    ret, image = video.read()

    if not ret:
        break


    plt_im=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray[gray>0]=1
    gray=np.logical_not(gray)
    gray=binary_erosion(gray)
    
    labeled=label(gray)

    if not ret:
        break


    cv2.imshow("Image", image)

    
    if labeled.max()==1:
        # plt.clf()
        frames+=1
        # plt.title("FOUND!!!!!")

        # plt.subplot(121)
        # plt.imshow(plt_im)
        # plt.subplot(122)
        # plt.imshow(gray)
        # plt.tight_layout()
        # plt.savefig(saving_path/f"{frames}.png")


    key=cv2.waitKey(1)
    

    if  key == ord("q"):
        break

print(frames)
cv2.destroyAllWindows()