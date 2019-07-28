import cv2
from _processing.color_mask import color_mask
from _processing.mask_info import mask_info
from _processing.path_detection import path_detection
from _utils.draw_shapes import draw_shapes
from _processing.roi import roi

mask={}
centroids={}

def cycle(vision, tasks):
    draw_q={'lines':[],'circle':[],'rectangle':[],'contour':[],'text':[]}

    for task in {'gate','path','bouy','torpedo','dropper'}:
        task = tasks[task]
        task._track(vision._frame)
        if task._detection_state:
            bbox=task._bbox
            R={'p1':(int(bbox[0]),int(bbox[1])),'p2':(int(bbox[0])+int(bbox[2]),int(bbox[1])+int(bbox[3])),'color':(0,0,255)}
            draw_q['rectangle'].append(R)
            setattr(vision._msg,task._name, True)
            R=roi(vision._frame,task._bbox)
            R= cv2.cvtColor(R, cv2.COLOR_BGR2HSV)
            mask[task._name] = color_mask(R,task._colors)
            cv2.imshow('R',mask[task._name])
            centroids[task._name], mask_bbox= mask_info(mask[task._name],draw_q,int(bbox[0]),int(bbox[1]))
            bbox=mask_bbox
            R={'p1':(int(bbox[0]),int(bbox[1])),'p2':(int(bbox[0])+int(bbox[2]),int(bbox[1])+int(bbox[3])),'color':(0,255,0)}
            draw_q['rectangle'].append(R)

    draw_shapes(vision._drawn,draw_q)
