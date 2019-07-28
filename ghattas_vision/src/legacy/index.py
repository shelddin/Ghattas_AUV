#!/usr/bin/env python
import cv2
from color_mask import color_mask
from path_detection import path_detection
from motion_tracking import motion_tracking
from draw_shapes import draw_shapes
#from dice import kme
from imutils.video import VideoStream
from FPS import FPS


#initializing basic variables to be shared and used throughout the code
colors = ['red','green','black','yellow','orange']
draw_q={'lines':[],'circle':[],'rectangle':[],'contour':[],'text':[]}
mask={}
# object tracking variables
centroids={}
back_track={}
for color in colors:
    back_track[color]=[]



# capture video feed from webcam
fps=FPS()
cap = VideoStream(src='../test_media/source.mp4').start()

while True:
    #read next frame from webcam
    frame = cap.read()
    #frame = cv2.imread('path.jpg')
    #check if frame has been read correctly
    if frame is None:
        print('video feed is lost :(')
        cv2.waitKey(0)
        break
    #pre process image
    frame=cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #analyse frame using color masks
    for color in colors:
        #color isolation (masking) and object detection(contours,boundary box, centroid)
        mask[color], centroids[color], contours = color_mask(hsv,color,draw_q)
        back_track[color]=motion_tracking(draw_q,back_track[color],centroids[color])
#       if color in {'black'} and len(c[color]) > 4:
#            kme(centroids[color],draw_q)
        if color in {'orange'}:
            path_detection(contours,draw_q)
#        cv2.imshow(color +' mask',mask[color])

    drawn,draw_q=draw_shapes(frame,draw_q)
    cv2.imshow('drawn',drawn)
    fps.update()


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
cap.stop()
