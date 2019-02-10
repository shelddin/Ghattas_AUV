import numpy as np
import cv2

def roi(frame,bbox):
    R = frame[int(bbox[1]):int(bbox[1]) + int(bbox[3]),int(bbox[0]):int(bbox[0]) + int(bbox[2])]
    return R
