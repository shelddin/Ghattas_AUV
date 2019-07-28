import cv2
import numpy as np


def mask_info(mask):
    #initialize & optain parameters
    min_size = 500
    approx= []
    bbox = []
    centroids= []
    first=True

    # find contours from the mask
    contours,hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        #check if contour fits the size thresholded
        if cv2.contourArea(c) < min_size:
            break

        #find approximated contour
        epsilon = 0.01 * cv2.arcLength(c, True)
        a = cv2.approxPolyDP(c, epsilon, True)
        approx.append(a)

        #find bounding box
        (x,y,w,h) = cv2.boundingRect(a)
        bbox.append((x,y,w,h))

        # compute the centroid of the contour & bounding box
        bX = int(w/2)+x
        bY = int(h/2)+y

        #add contour center to centers array
        centroids.append((bX,bY))


    return centroids,bbox, approx
