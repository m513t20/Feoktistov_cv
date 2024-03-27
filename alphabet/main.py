import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

from skimage import draw

from skimage.measure import label,regionprops

from skimage.filters import threshold_otsu

from collections import defaultdict

def filling_factor(arr):
    return np.sum(arr)/arr.size


def has_vline(arr,width=1):
    return width<=np.sum(arr.mean(0)==1)



def count_holes(region):
    labeled=label(np.logical_not(region))
    regions=regionprops(labeled)
    holes=0
    for region in regions:
        flag=1
        coords=np.where(labeled==region.label)
        for y,x in zip(*coords):
            if y==0 or x==0 or y==labeled.shape[0]-1 or  x==labeled.shape[1]-1:
                flag=0
        holes+=flag
    return holes

def recognize(region): 
    if filling_factor(region.image)==1.0:
        return '-'
    else:
        holes=count_holes(region.image)
        if holes==2:#8 B
            if has_vline(region.image,3):
                return "B"
            else:
                return"8" 
        elif holes==1:#A 0
            ny,nx=region.local_centroid[0]/region.image.shape[0],region.local_centroid[1]/region.image.shape[1]
            print(ny/nx)
            if np.isclose(ny,nx,0.092):
                if has_vline(region.image,3):
                    return "P"
                return "0"



            else:
                if has_vline(region.image,3):
                    return "D"


                return "A"
        else:
            if has_vline(region.image):
                return "1"
            else: #W, X ,*,/
                framed=region.image.copy()

                framed[0,:]=1
                framed[-1,:]=1
                framed[:,0]=1
                framed[:,-1]=1
                holes=count_holes(framed)
                if region.eccentricity<0.4:
                    return"*"
                match holes:
                    case 2: return "/"
                    case 4: return "X"
                    case _: return "W"
            
    return "_"

    


def hist(arr):
    result=np.zeros(256)
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            result[arr[y,x]]+=1

    return result

image=plt.imread("symbols.png").mean(2)

image[image>0]=1

regions=regionprops(label(image))

symbols=len(regions)

result=defaultdict(lambda:0)

for i,region in enumerate(regions):
    symbol=recognize(region)
    result[symbol]+=1

    
print(result)
