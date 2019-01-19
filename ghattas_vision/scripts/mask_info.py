import imutils
import cv2
import numpy as np
import param


def mask_info(mask,color,draw_q):
    #initialize & optain parameters
    min_size = param.contour_min_size(color)
    approx= []
    centroids= []

    # find contours from the mask
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Don't worry about it, it fixes a bug, and yes it's copy paste but it works!!
    contours = contours[0] if imutils.is_cv2() else contours[1]


    #process all contours
    for c in contours:
        #check if contour fits the size thresholded
        if cv2.contourArea(c) > min_size:
            #find approximated contour
            epsilon = 0.01 * cv2.arcLength(c, True)
            a = cv2.approxPolyDP(c, epsilon, True)
            approx.append(a)

            #find rotated bounding box
            rect = cv2.minAreaRect(a)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            #find bounding box
            x,y,w,h = cv2.boundingRect(c)

            # compute the centroid of the contour & bounding box
            M = cv2.moments(a)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            bX = int(w/2)+x
            bY = int(h/2)+y

            #add contour center to centers array
            centroids.append((bX,bY))

            # add to draw que
            if draw_q != None:
                #Co1={'cont':[box],'color':(255,0,0)}
                #draw_q['contour'].append(Co1)
                #C1={'center':(int(rect[0][0]), int(rect[0][1])),'radius':6,'color':(255, 0, 0)}
                #draw_q['circle'].append(C1)
                #Co2={'cont':[a],'color':(0, 255, 0)}
                #draw_q['contour'].append(Co2)
                #C2={'center':(cX,cY),'radius':4,'color':(0, 255, 0)}
                #draw_q['circle'].append(C2)
                R={'p1':(x,y),'p2':(x+w,y+h),'color':(0,255,0)}
                draw_q['rectangle'].append(R)
                C3={'center':(bX,bY),'radius':2,'color':(0, 255, 0)}
                draw_q['circle'].append(C3)
                T={'text':color,'p':(bX - 20, bY - 20),'color':(255, 255, 255)}
                draw_q['text'].append(T)


    return centroids,approx
