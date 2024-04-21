import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import cv2
import os
from skimage.measure import label,regionprops

from collections import defaultdict


def has_vline(arr,width=1):
    return width<=np.sum(arr.mean(0)==1)



def get_shapes(regions):

    shapes=defaultdict(lambda:0)

    for index,region in enumerate(regions):
        key=''

        eccent=region.eccentricity
        if eccent==0:
            if (region.image.size==region.area):
                key='sqare'
            else:
                key='circle'
        else:
            key='rectangle'

        # plt.clf()
        # plt.title(f"symbol={key}")
        # plt.imshow(region.image)
        # plt.tight_layout()
        # plt.savefig(Path(__file__).parent/"figs"/f"{index}.png")

        shapes[key]+=1

    return shapes


def get_colors(img):
   
    colors=[]

    for cur_val in np.unique(img):
        tmp_img=np.copy(img)
        tmp_img[tmp_img!=cur_val]=0
        tmp_img[tmp_img>0]=1

        labeled=label(tmp_img)

        m_col=labeled.max()
        colors.append(m_col)
    return colors

file=Path(__file__).parent/"balls_and_rects.png"

image=plt.imread(file)




bin_image=np.mean(image,2)
bin_image[bin_image>0]=1
labeled=label(bin_image)
regions=regionprops(labeled)




print(f'overall figures={labeled.max()}')

shapes=get_shapes(regions)
for cur_key in shapes:
    print(f'figures shaped like {cur_key} = {shapes[cur_key]}')


colored_image=np.mean(image,2)
colors=get_colors(colored_image)
for index,value in enumerate(colors):
    if index==0:
        continue
    print(f'color № {index} = {value}')



