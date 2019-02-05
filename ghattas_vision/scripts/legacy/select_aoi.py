import cv2
import numpy as np

pointIndex=0
pts=[]
img=None

def click_cb(event,x,y,flags,param):
    global img
    global pointIndex
    global pts

    if event == cv2.EVENT_LBUTTONDBLCLK:
        print('new point selected {}'.format((x,y)))
        cv2.circle(img,(x,y),0,(255,0,0),-1)
        pts.append((x,y))
        pointIndex = pointIndex + 1


def select_aoi(frame):
    global img
    global pointIndex
    global pts
    img=frame
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',click_cb)
    while True:
        for pt in pts:
            cv2.circle(img,(pt[0],pt[1]),4,(255,0,0),-1)
        cv2.imshow('image',img)
        if(pointIndex==4):
            pts=np.array(pts)
            return pts
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


#cap=cv2.VideoCapture(0)
#_,frame = cap.read()
#select_aoi(frame)
#cap.release()
#cv2.destroyAllWindows()
