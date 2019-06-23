#!/usr/bin/env python
import cv2
from FPS import FPS
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
from stereo_msgs.msg import DisparityImage
from zed_calibration import *


def callback(data):
    disp_real = bridge.imgmsg_to_cv2(data.image, desired_encoding="passthrough")
    world_pts = cv2.reprojectImageTo3D(disp_real, Q,handleMissingValues=True)
    world_pts_msg = bridge.cv2_to_imgmsg(world_pts, "passthrough")
    world_pts_pub.publish(world_pts_msg)
    cv2.waitKey(1)

rospy.init_node("zed_driver")
imgL_pub = rospy.Publisher("/zed/left/image_raw",Image, queue_size=10)
imgR_pub = rospy.Publisher("/zed/right/image_raw",Image, queue_size=10)
camL_pub = rospy.Publisher("/zed/left/camera_info",CameraInfo, queue_size=10)
camR_pub = rospy.Publisher("/zed/right/camera_info",CameraInfo, queue_size=10)

world_pts_pub = rospy.Publisher("/zed/world_pts",Image, queue_size=10)
rospy.Subscriber("/zed/disparity", DisparityImage, callback)

bridge = CvBridge()

cam_infoL = CameraInfo()
cam_infoL.height = CAMERA_HEIGHT
cam_infoL.width = CAMERA_WIDTH/2
cam_infoL.distortion_model = "plumb_bob"
cam_infoL.K = KL
cam_infoL.D = DL
cam_infoL.R = RL
cam_infoL.P = PL

cam_infoR = CameraInfo()
cam_infoR.height = CAMERA_HEIGHT
cam_infoR.width = CAMERA_WIDTH/2
cam_infoR.distortion_model = "plumb_bob"
cam_infoR.K = KR
cam_infoR.D = DR
cam_infoR.R = RR
cam_infoR.P = PR

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

fps = FPS()

while True:
    _,frame=cap.read()

    if frame != None:
        height, width, channels = frame.shape
        frameL=frame[0:height,0:width/2]
        frameR=frame[0:height,width/2:width]

        imgL_pub.publish(bridge.cv2_to_imgmsg(frameL, "bgr8"))
        imgR_pub.publish(bridge.cv2_to_imgmsg(frameR, "bgr8"))

        camL_pub.publish(cam_infoL)
        camR_pub.publish(cam_infoR)

        cv2.imshow("frame", cv2.resize(frameL, (0,0), fx=0.1, fy=0.1))
        fps.update()

        k=cv2.waitKey(1)
        if k== 27:
            break
