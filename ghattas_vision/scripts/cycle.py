import cv2
from color_mask import color_mask
from path_detection import path_detection
from motion_tracking import motion_tracking
from draw_shapes import draw_shapes

mask={}
centroids={}

def cycle(vision):
    draw_q={'lines':[],'circle':[],'rectangle':[],'contour':[],'text':[]}

    #frame = cv2.resize(vision._frame, (0,0), fx=0.25, fy=0.25)
    hsv = cv2.cvtColor(vision._frame, cv2.COLOR_BGR2HSV)
    for color in vision._mode_config['colors']:
        mask[color], centroids[color], contours = color_mask(hsv,color,draw_q)
        if color == 'red':
            vision._reset_target_msg()
            if len(centroids[color]) != 0:
                vision._detection_out.gate = True
                vision._target_out.found=True
                vision._target_out.x=centroids[color][0][0]
                vision._target_out.z=centroids[color][0][1]
            vision._publish('gate',vision._target_out)
#        back_track[color]=object_tracking(draw_q,back_track[color],centroids[color])
#        if color in {'orange'}:
#            path_detection(contours,draw_q)
    draw_shapes(vision._drawn,draw_q)
