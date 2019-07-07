import cv2
import _param.processing_param as param
import rospy
import numpy as np

def get_range(color):
    range = [[],[]]
    range[0]=[rospy.get_param("/vision_param/"+color+"_heu_lower"),
    rospy.get_param("/vision_param/"+color+"_saturation_lower"),
    rospy.get_param("/vision_param/"+color+"_value_lower")]

    range[1]=[rospy.get_param("/vision_param/"+color+"_heu_upper"),
    rospy.get_param("/vision_param/"+color+"_saturation_upper"),
    rospy.get_param("/vision_param/"+color+"_value_upper")]

    return np.array([range])


def color_mask(frame,colors):
    #initialize & optain parameters
    kernel_size= (5,5)
    first=True
    mask=None
    #range = param.color_thresh['green']

    for color in colors:
        #range=param.color_thresh[color]
        range = get_range(color)

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

    return mask
