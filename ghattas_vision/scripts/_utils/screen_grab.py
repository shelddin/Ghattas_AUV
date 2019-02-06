import numpy as np
import cv2
import mss

monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
def screen_grab(area = monitor):
	with mss.mss() as sct:
		return np.array(sct.grab(area))
