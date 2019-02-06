import cv2
from mask_info import mask_info
import _param.processing_param

def color_mask(frame,color,draw_q=None):
    #initialize & optain parameters
    range=param.color_thresh[color]
    kernel_size= param.kernel_size
    first=True

    #in case of multiple ranges given for a color itirate for every range and compine all masks
    for r in range:
        #add the new color range mask to the total mask
        if first == True:
            mask = cv2.inRange(frame, r[0], r[1])
            mask = cv2.erode(mask,kernel_size)
            mask = cv2.dilate(mask,kernel_size)
            first=False
        #first color range mask
        else:
            mask_it = cv2.inRange(frame, r[0], r[1])
            mask_it = cv2.erode(mask_it,kernel_size)
            mask_it = cv2.dilate(mask_it,kernel_size)
            mask = cv2.bitwise_or(mask, mask_it)
    #object detection(contours,boundary box, centroid)
    centroids,contours = mask_info(mask,color,draw_q)

    return mask,centroids,contours
