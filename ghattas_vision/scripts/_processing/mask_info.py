import imutils
import cv2
import numpy as np
import _param.processing_param


def mask_info(mask,color,draw_q):
    #initialize & optain parameters
    min_size = param.contour_min_size(color)
    approx= []
    centroids= []

    # find contours from the mask
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Don't worry about it, it fixes a bug, and yes it's copy paste but it works!!
    contours = contours[0] if imutils.is_cv2() else contours[1]
    contours = sorted(cnts, key=cv2.contourArea, reverse=True)

    #process all contours
    #for c in contours:
        #check if contour fits the size thresholded
        #if cv2.contourArea(c) < min_size:
            #break
    c=contours[0]
    #find bounding box
    x,y,w,h = cv2.boundingRect(c)
    bbox={'x':x,'y':y,'w':w,'h':h}
    approx.append(bbox)

    # compute the centroid of the contour & bounding box
    bX = int(w/2)+x
    bY = int(h/2)+y

    #add contour center to centers array
    centroids.append((bX,bY))

    # add to draw que
    if draw_q != None:
        R={'p1':(x,y),'p2':(x+w,y+h),'color':(0,255,0)}
        draw_q['rectangle'].append(R)
        C3={'center':(bX,bY),'radius':2,'color':(0, 255, 0)}
        draw_q['circle'].append(C3)
        T={'text':color,'p':(bX - 20, bY - 20),'color':(255, 255, 255)}
        draw_q['text'].append(T)


    return centroids,bbox
