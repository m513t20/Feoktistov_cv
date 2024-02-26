import numpy as np
import matplotlib.pyplot as plt
import socket

host="84.237.21.36"
port=5152

def neighbours8(y,x):
    return (y,x-1),(y-1,x),(y,x+1),(y+1,x),(y-1,x-1),(y-1,x+1),(y+1,x-1),(y+1,x+1)

def recall(sock,n):
    data=bytearray()
    while(len(data)<n):
        packet=sock.recv(n-len(data))
        if not packet:
            return
        data.extend(packet)

    return data 

def check(Arr,y,x):

    for i in neighbours8(y,x):
        if Arr[y][x]<=Arr[i[0]][i[1]]:
            return False
    return True




with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    sock.connect((host,port))
    for i in range(10):
        sock.send(b"get")

        bts=recall(sock,40002)
        #print(len(bts))

        im1=np.frombuffer(bts[2:40002],dtype="uint8").reshape(bts[0],bts[1])

        maxes=np.array([[0,0],[0,0]])
        i=0
        for y in range(im1.shape[0]):
            for x in range(im1.shape[1]):
                if check(im1,y,x):
                    maxes[i]=[y,x]
                    i+=1
        #print(maxes)
                    
        dist=np.sqrt((maxes[0][0]-maxes[1][0])**2+(maxes[0][1]-maxes[1][1])**2)

        #print(dist)
    

        # pos1=np.unravel_index(np.argmax(im1)[0],im1.shape)
        
        # pos2=np.unravel_index(np.argmax(im1)[0],im1.shape)


        # res=np.abs(np.array(pos1)-np.array(pos2))

        sock.send(f"{round(dist,1)}".encode())
        
        print(sock.recv(20))



    sock.send(b"beat")

    print(sock.recv(20))


plt.subplot(121)

plt.imshow(im1)



plt.show()
