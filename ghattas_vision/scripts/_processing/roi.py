import numpy as np
import cv2

def roi(frame,bbox):
    R = frame[bbox.y:bbox.y + bbox.h,bbox.x:bbox.x + bbox.w]
    return R
