#!/usr/bin/env python
import cv2
import rospy
import time
import os

from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Point
from ghattas_vision.msg import vision_task_detection
from cv_bridge import CvBridge, CvBridgeError

from _processing.get_position import get_position
from _processing.template_matcher import template_matcher
from _processing.color_mask import color_mask
from _processing.mask_info import mask_info

def bouy(name):
    template_path=os.path.dirname(os.path.abspath(__file__))+'/templates/'+name+'.jpeg'
    bbox = template_matcher(color, template_path)
    position = get_position(depth, bbox)

    cv2.rectangle(color, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 0, 255), 2)
    cv2.putText(color, name+':'+str(position), (bbox[0], bbox[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)

    print("bouy " + name + " position"+str(position))

def torpedo():
    template_path=os.path.dirname(os.path.abspath(__file__))+'/templates/torpedo.jpeg'
    template_bbox = template_matcher(color, template_path)
    position = get_position(depth, template_bbox)

    mask = color_mask(hsv, ['green'])
    centroids, contour_bbox, contours = mask_info(mask)

    cv2.drawContours(color,contours,-1,(0,255,0),10)
    for bbox in contour_bbox:
        cv2.rectangle(color, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 0, 255), 2)

    cv2.rectangle(color, (template_bbox[0], template_bbox[1]), (template_bbox[0]+template_bbox[2], template_bbox[1]+template_bbox[3]), (0, 0, 255), 2)
    cv2.putText(color, 'torpedo:'+str(position), (template_bbox[0], template_bbox[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 2)




def process():
    global color_availability,position, hsv
    color_availability = False
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    cv2.imshow('depth', depth)

    #bouy('gench')
    torpedo()

    cv2.imshow('color', color)
    k = cv2.waitKey(1)
    if k==ord('s') or k==ord('t'):
        bbox = cv2.selectROI('color', color)
        print ("saving image")
        saved = cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+'/templates/'+str(time.time()) + '.jpeg', color[int(bbox[1]):int(bbox[1]) + int(bbox[3]),int(bbox[0]):int(bbox[0]) + int(bbox[2])])
        print("saved:"+ str(saved))





def publish(msg, publisher):
    publishers[publisher].publish(msg)




def depthCB(data):
    global depth
    depth = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    if color_availability:
        process()


def colorCB(data):
    global color_availability, color
    color = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    color_availability = True



global bridge, depth, color, depth_availability, color_availability, publishers, position
bridge = CvBridge()
color_availability = False
depth = None
color = None
hsv = None
position = None

rospy.init_node("vision_node")

rospy.Subscriber("/zed/world_pts", Image, depthCB)
rospy.Subscriber("/zed/left/image_rect_color", Image, colorCB)

publishers = {}
publishers['detected'] = rospy.Publisher('zed/detected', vision_task_detection, queue_size=10, latch=True)
for publisher in []:
    publishers[publisher] = rospy.Publisher('zed/' + publisher, Point, queue_size=10, latch=True)

rospy.spin()
