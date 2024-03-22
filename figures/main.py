import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face
from skimage.measure import label
from skimage.morphology import binary_closing,binary_erosion,binary_opening,binary_dilation
from pathlib import Path




def neighbours8(y,x):
    return (y,x-1),(y-1,x),(y,x+1),(y+1,x),(y-1,x-1),(y-1,x+1),(y+1,x-1),(y+1,x+1)



def get_boundaries(LB,label=1):
    pos=np.where(LB==label)

    bounds=[]
    for y,x in zip(*pos):
        for yn,xn in neighbours8(y,x):
            if yn<0 or xn>LB.shape[0]-1:
                bounds.append((y,x))
                break
            elif yn>LB.shape[1]-1 or xn<0:
                bounds.append((y,x))
                break
            elif LB[yn,xn]==0:
                bounds.append((y,x))
                break

    return bounds

def get_shape(bounds):
    ymin,xmin=bounds[0][0],bounds[0][1]
    LB=np.array([[0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]])
    for y,x  in bounds:
        LB[y-ymin,x-xmin]=1 
    return LB



#изначально был вариант динамически находить формы для эрозии, но это долго - вот функция по которой я нашёл маски
def get_shapes(image):
    
    labeled=label(image)

    bound=np.copy(image)
    types=set()
    for i in range(1,np.max(labeled)):
        cur_shape=(get_shape(get_boundaries(labeled,i)))

        len_chek=len(types)

        types.add(label(binary_erosion(bound,cur_shape)).max())
        


        if len(types)!=len_chek:
            print(cur_shape)



type1=np.array([[1,1,1,1,1,1]
                ,[1,1,1,1,1,1]
                ,[1,1,1,1,1,1]
                ,[1,1,1,1,1,1]
                ,[0,0,0,0,0,0]
                ,[0,0,0,0,0,0]])



type2=np.array([[1,1,1,1,0,0]
                ,[1,1,1,1,0,0]
                ,[0,0,1,1,0,0]
                ,[0,0,1,1,0,0]
                ,[1,1,1,1,0,0]
                ,[1,1,1,1,0,0]])
        


type3=np.array([[1,1,0,0,1,1]
                ,[1,1,0,0,1,1]
                ,[1,1,1,1,1,1]
                ,[1,1,1,1,1,1]
                ,[0,0,0,0,0,0]
                ,[0,0,0,0,0,0]])
                        


type4=np.array([[1,1,1,1,1,1]
                ,[1,1,1,1,1,1]
                ,[1,1,0,0,1,1]
                ,[1,1,0,0,1,1]
                ,[0,0,0,0,0,0]
                ,[0,0,0,0,0,0]])
        

type5=np.array([[1,1,1,1,0,0],
                [1,1, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0, 0,],
                [1, 1, 1, 1, 0, 0]])
                        



image=np.load(Path(__file__).parent/"ps.npy.txt")


labeled=label(image)

print(f'overall figures= {labeled.max()}')

tmp=binary_dilation(binary_erosion(image,type1),type1)

print(f'type 1 {label(tmp).max()}')

image-=tmp

tmp=binary_dilation(binary_erosion(image,type2),type2)

print(f'type 2 {label(tmp).max()}')

image-=tmp

tmp=binary_dilation(binary_erosion(image,type3),type3)

print(f'type 3 {label(tmp).max()}')

image-=tmp

tmp=binary_dilation(binary_erosion(image,type4),type4)

print(f'type 4 {label(tmp).max()}')

image-=tmp

tmp=binary_dilation(binary_erosion(image,type5),type5)

print(f'type 5 {label(tmp).max()}')

image-=tmp








# plt.imshow(labeled)

# plt.show()