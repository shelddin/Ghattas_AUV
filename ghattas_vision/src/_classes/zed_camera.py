import cv2
from imutils.video import VideoStream
from FPS import FPS
import numpy as np
from _param.zed_calibration import *
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

CAMERA_HEIGHT=720
CAMERA_WIDTH=2560

# FILTER Parameters
lmbda = 80000
sigma = 1.2
visual_multiplier = 1.0

class zed_camera(object):
    """docstring for zed_camera."""

    def __init__(self, arg):
        super(zed_camera, self).__init__()
        #cap = VideoStream(src=0, resolution=(2560,720)).start()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.fps = FPS()

        self.imgUL = None
        self.imgUR = None

        rospy.init_node("stereo_streamer")
        self.imgL_pub = rospy.Publisher("imgL",Image, queue_size=10)
        self.imgR_pub = rospy.Publisher("imgR",Image, queue_size=10)


        self.left_matcher = cv2.StereoSGBM_create(
            minDisparity=0,
            numDisparities=160,             # max_disp has to be dividable by 16 f. E. HH 192, 256
            blockSize=5,
            disp12MaxDiff=1,
            uniquenessRatio=15,
            speckleWindowSize=0,
            speckleRange=2,
            preFilterCap=63,
            mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
        )

        self.right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

        self.wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
        self.wls_filter.setLambda(lmbda)
        self.wls_filter.setSigmaColor(sigma)

        self.mapLx, self.mapLy = cv2.initUndistortRectifyMap(camera_matrix_L, dist_coeff_L, RL, PL, (2560/2, 720), cv2.CV_32FC1)

        self.mapRx, self.mapRy = cv2.initUndistortRectifyMap(camera_matrix_R, dist_coeff_R, RR, PR, (2560/2, 720), cv2.CV_32FC1)

    def read(self):
    	_,frame= self.cap.read()
    	height, width, channels = frame.shape
    	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	frameL=frame[0:height,0:width/2]
    	self.imgUL = cv2.resize(cv2.remap(frameL, self.mapLx, self.mapLy, cv2.INTER_LINEAR), (0,0), fx=0.5, fy=0.5)
    	frameR=frame[0:height,width/2:width]
    	self.imgUR = cv2.resize(cv2.remap(frameR, self.mapRx, self.mapRy, cv2.INTER_LINEAR), (0,0), fx=0.5, fy=0.5)

    	displ = self.left_matcher.compute(imgUL, imgUR)  # .astype(np.float32)/16
    	dispr = self.right_matcher.compute(imgUR, imgUL)
    	displ = np.int16(displ)
    	dispr = np.int16(dispr)

    	filteredImg = self.wls_filter.filter(displ, imgUL, None, dispr)
    	filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    	filteredImg = np.uint8(filteredImg)

    	self.fps.update()

    def streem(self):
        self.imgL_pub.publish(bridge.cv2_to_imgmsg(self.imgUL, "bgr8"))
        self.imgR_pub.publish(bridge.cv2_to_imgmsg(self.imgUR, "bgr8"))
