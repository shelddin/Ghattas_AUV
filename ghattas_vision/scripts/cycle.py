import cv2
from _processing.color_mask import color_mask
from _processing.path_detection import path_detection
from _utils.draw_shapes import draw_shapes
from _processing.roi import roi

mask={}
centroids={}

def cycle(vision, tasks):
    draw_q={'lines':[],'circle':[],'rectangle':[],'contour':[],'text':[]}

    for task in tasks:
        task._track(vision._frame)
        if task._detection_state:
            vision._msg[task._name]=True
            R=roi(vision._frame,task._bbox)
            R= cv2.cvtColor(vision._frame, cv2.COLOR_BGR2HSV)
            for color in task._colors:
                mask[color], centroids[color], task._bbox = color_mask(R,color,draw_q)

    draw_shapes(vision._drawn,draw_q)
