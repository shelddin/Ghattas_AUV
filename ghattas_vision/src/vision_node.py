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

def bouy_gench():
    template_path=os.path.dirname(os.path.abspath(__file__))+'/templates/bouy_gench.jpeg')
    bbox = template_matcher(color,"bouy_gench", template_path)
    position = get_position(depth, bbox, color)
    print("bouy gench position"+str(position))
    
    
    
    
def process():
    global color_availability,position
    color_availability = False
    cv2.imshow('color', color)
    cv2.imshow('depth', depth)
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
position = None

rospy.init_node("vision_node")

rospy.Subscriber("/zed/world_pts", Image, depthCB)
rospy.Subscriber("/zed/left/image_rect_color", Image, colorCB)

publishers = {}
publishers['detected'] = rospy.Publisher('zed/detected', vision_task_detection, queue_size=10, latch=True)
for publisher in []:
    publishers[publisher] = rospy.Publisher('zed/' + publisher, Point, queue_size=10, latch=True)

rospy.spin()
