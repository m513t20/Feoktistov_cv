import cv2
from random import shuffle


code=['r','g','b','y']
shuffle(code)

print(code[0],code[1])
print(code[2],code[3])


camera=cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
camera.set(cv2.CAP_PROP_EXPOSURE,-4)



cv2.namedWindow("Image",cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask",cv2.WINDOW_GUI_NORMAL)

lower={'r':(160,160,150),'b':(80,160,150),'g':(57,100,160),'y':(15,170,190)}
upper={'r':(195,255,255),'b':(110,255,255),'g':(75,255,255),'y':(30,255,255)}
colors={'r':(0,0,255),'b':(255,0,0),'g':(0,255,0),'y':(0,255,255)}

def get_balls(blurred,key):
    global lower
    global upper
    global colors
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    mask=cv2.inRange(hsv,lower[key],upper[key])
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)


    cnts=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    
    if len(cnts)>0:
        c=max(cnts,key=cv2.contourArea)
        (cur_x,cur_y),r=cv2.minEnclosingCircle(c)
        if r>10:
            cv2.circle(image,(int(cur_x),int(cur_y)), int(r),colors[key],2)
            return (cur_x,cur_y)
        
    return None




roi=None
    #red 170+ 110-120 220-240
    #blue 90 40 255
while camera.isOpened():
    officer={}
    _,image=camera.read()
    blurred=cv2.GaussianBlur(image,(11,11),0)
 
    for key in list(lower.keys()):
        balls=get_balls(blurred,key)
        if balls is not None:
            officer[key]=balls
    

    if len(list(officer.keys()))==4:
        answer=[]
        ans_y=[]
        for key in code:
            answer.append(officer[key][0])
            ans_y.append(officer[key][1])
        test_y=(ans_y[0]<ans_y[2] and ans_y[0]<ans_y[3]) and(ans_y[1]<ans_y[2] and ans_y[1]<ans_y[3]) 
        check_1_row=[answer[0],answer[1]]
        check_2_row=[answer[2],answer[3]]
        check_1_row.sort()
        check_2_row.sort()
        if check_1_row==answer[:2] and check_2_row==answer[2:4] and test_y :
            print('YAY! YOU DID IT!')
            cv2.putText(image,f"YAY! YOU DID IT!",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(127,255,255))


    key=cv2.waitKey(1)
    if key == ord('q'):
        break

    cv2.imshow("Image",image)

camera.release()
cv2.destroyAllWindows()