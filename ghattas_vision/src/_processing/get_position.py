import cv2
import numpy as np

def get_position(depth, bbox, color):
    height, width, _ = color.shape
    mask1 = np.zeros((height,width), np.uint8)
    mask1[int(bbox[1]):int(bbox[1]) + int(bbox[3]),int(bbox[0]):int(bbox[0]) + int(bbox[2])]=(1)
    mask2 = cv2.inRange(depth, np.array([0,0,0]), np.array([50,50,50]))
    mask = cv2.bitwise_and(mask1, mask2)

    position = cv2.mean(depth, mask)
    return position
