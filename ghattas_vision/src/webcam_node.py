#!/usr/bin/env python
import cv2
import rospy
import numpy as np
#from imutils.video import VideoStream
from _utils.FPS import FPS

from _processing.color_mask import color_mask
from _processing.mask_info import mask_info
from _processing.path_detection import path_detection


def path(hsv):
    mask = color_mask(hsv, ['orange'])
    centroids,bbox, contours = mask_info(mask)
    cv2.drawContours(frame,contours,-1,(0,255,0),10)
    if contours != None:
        path = path_detection(contours)
        print(path)
        if path != None:
            cv2.line(frame,path[0][0],path[0][1],(255,0,0),10)
            cv2.line(frame,path[1][0],path[1][1],(255,0,0),10)

    cv2.imshow('path mask', cv2.resize(mask, (0,0), fx=0.5, fy=0.5))


#cap = VideoStream(src=2).start()
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fps = FPS()


while True:

    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    path(hsv)

    cv2.imshow('frame', cv2.resize(frame, (0,0), fx=0.5, fy=0.5))

    fps.update()

    k = cv2.waitKey(0)
    if k == ord('q'):
        break
