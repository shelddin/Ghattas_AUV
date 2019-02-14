import imutils
import cv2
import numpy as np
import _param.processing_param as param


def mask_info(mask,draw_q,x_shift,y_shift,color='black'):
    #initialize & optain parameters
    min_size = param.contour_min_size(color)
    approx= []
    centroids= []
    first=True
    bbox=None
    # find contours from the mask
    contours,hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        #check if contour fits the size thresholded
        if cv2.contourArea(c) > min_size:
            #find bounding box
            (x,y,w,h) = cv2.boundingRect(c)
            approx.append((x,y,w,h))

            # compute the centroid of the contour & bounding box
            bX = int(w/2)+x
            bY = int(h/2)+y

            #add contour center to centers array
            centroids.append((bX,bY))
            # add to draw que
            if draw_q != None:
                R={'p1':(x,y),'p2':(x+w,y+h),'color':(255,0,0)}
                draw_q['rectangle'].append(R)
                C3={'center':(bX,bY),'radius':2,'color':(255, 0, 0)}
                draw_q['circle'].append(C3)


            x=x+x_shift
            y=y+y_shift

            if first:
                x1,y1,x2,y2 = x,y,x+w,y+h
                first=False
            else:
                if x < x1:
                    x1 = x

                if y < y1:
                    y1 = y

                if x+w > x2:
                    x2 = x+w

                if y+h > y2:
                    y2 = y+h

    if not first:
        x,y,w,h=x1,y1,x2-x1,y2-y1
        bbox = (x,y,w,h)


    return centroids,bbox
