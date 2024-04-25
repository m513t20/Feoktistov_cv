import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from skimage.measure import label,regionprops
from skimage.color import rgb2hsv
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
                key='rectangle'
            else:
                key='circle'
        else:
            key='rectangle'


        shapes[key]+=1

    return shapes


file=Path(__file__).parent/"balls_and_rects.png"

image=plt.imread(file)




bin_image=np.mean(image,2)
bin_image[bin_image>0]=1
labeled=label(bin_image)


print(f'overall figures={labeled.max()}')



hsv_image=rgb2hsv(image)


c=0
prev=0
ars=[[],[],[],[],[],[],[],[],[],[]]
for index,i in enumerate(np.linspace(0,1,10)):
    tmp_image=np.copy(hsv_image)
    tmp_image[tmp_image[:,:,0]<prev]=0
    tmp_image[tmp_image[:,:,0]>i]=0
    tmp_image[tmp_image[:,:,0]>0]=1

    tmp_image=np.mean(tmp_image,2)

    labeled=label(tmp_image)
    if labeled.max()>0:
        c+=1
        print(f'color № {c}')
        regions=regionprops(labeled)
        shapes=get_shapes(regions)
        for cur_key in shapes:
            print(f'\tfigures shaped like {cur_key} = {shapes[cur_key]}')



    prev=i


