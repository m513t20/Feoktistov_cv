import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

from skimage import draw

from skimage.measure import label,regionprops

from skimage.filters import threshold_otsu

from collections import defaultdict

from skimage.morphology import binary_closing,binary_erosion,binary_opening,binary_dilation

def has_vline(arr,width=1):
    return width<=np.sum(arr.mean(0)==1)


def distance(p1,p2):
    return ((p1-p2)**2).sum()**0.5

def classificator(props,classes):
    klass=None
    min_d=10**16
    for cur_class in classes:
        d=distance(props,classes[cur_class])

        if d<min_d:
            klass=cur_class
            min_d=d

    return klass

def extr(region):
    area=region.area/region.image.size
    cy,cx=region.centroid_local
    cy/=region.image.shape[0]
    cx/=region.image.shape[1]
    eccentricity=region.eccentricity
    if eccentricity<0.4:
        eccentricity=-1
    perimeter=region.perimeter/region.image.size
    euler=region.euler_number
    V=has_vline(region.image,3)
    return np.array([area,cy,cx,eccentricity,perimeter,euler,V])

def hist(arr):
    result=np.zeros(256)
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            result[arr[y,x]]+=1

    return result


vals=[6,7,5,7,5,6,7,7,6,7,9,8]
directory=Path(__file__).parent/"images"

saved_pencils=open(directory/'pencils.txt','r')


#собрали данные по всем каранадашам и теперь сверяем с ними
data=[]
for i in range(21):
    args=saved_pencils.readline().split(',')
    args=list(map(float,args[:-1]))


    data.append(np.array(args))



ovrall=0

for i in range(1,13):
    image=plt.imread(directory/f'img ({i}).jpg')

    image=np.mean(image,2).astype("uint8")
    
    print(f'image={i}')
    

    thresh=threshold_otsu(image)

    image[image>thresh]=0

    # image[image>150]=0
    pencils=0

    image[image>0]=1


    mask=np.array([[0,1,0],
                   [1,1,1],
                   [0,1,0]])

    image=binary_opening(image)
    #image=binary_erosion(image,mask)

    while label(image).max()>vals[i-1]+2:
        image=binary_dilation(image)

    labeled=label(image)



    regions=regionprops(labeled)

    for region in regions:
        ex=extr(region)
        for cur_dat in data:

            
            if distance(cur_dat,ex)<0.008:
                pencils+=1
                break

    ovrall+=pencils
            
    print(f'Pencils={pencils}')


saved_pencils.close()
print(f'overall={ovrall}')


