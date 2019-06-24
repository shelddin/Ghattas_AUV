import cv2
import _param.processing_param as param

def color_mask(frame,colors):
    #initialize & optain parameters
    kernel_size= (5,5)
    first=True
    mask=None

    for color in colors:
        range=param.color_thresh[color]

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
