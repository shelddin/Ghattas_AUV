import numpy as np
import cv2

def roi(frame,x,y,h,w):
    R = frame[y:y + h,x:x + w]
    return R
