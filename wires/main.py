import numpy as np
import matplotlib.pyplot as plt
from scipy.datasets import face
from skimage.measure import label
from skimage.morphology import binary_closing,binary_erosion,binary_opening,binary_dilation

file='wires1.npy.txt'
mask=np.array([[0,1,0],
                [0,1,0],
                [0,1,0]])
for i in range(1,7):
    plt.subplot(2,3,i)
    image=np.load(f'wires{i}.npy.txt')
    print(f"file=wires{i}.npy.txt")

    lab_im=label(image)

    for cur_key in range(1,lab_im.max()+1):
        new_im=binary_erosion(lab_im==cur_key,mask)
        max_ind=np.max(label(new_im))
        match max_ind:
            case 1:
                print(f'wire {cur_key} is complete')
            case 0:
                print(f'wire {cur_key} is invalid')
            case _:
                print(f'wire {cur_key} split on', max_ind)



    plt.imshow(image)

plt.show()