import numpy as np
import cv2
from mss import mss
import time

mon = {'top': 160, 'left': 160, 'width': 800, 'height': 600}

sct = mss()

def screen_grab():
    img=np.array(sct.grab(mon))
    return img
