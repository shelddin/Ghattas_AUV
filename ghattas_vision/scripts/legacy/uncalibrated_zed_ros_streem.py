import cv2
from FPS import FPS
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


rospy.init_node("stereo_streamer")
imgL_pub = rospy.Publisher("imgL",Image, queue_size=10)
imgR_pub = rospy.Publisher("imgR",Image, queue_size=10)

bridge = CvBridge()

CAMERA_HEIGHT=720
CAMERA_WIDTH=2560

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

fps = FPS()

while True:
	_,frame=cap.read()
	height, width, channels = frame.shape
	frameL=frame[0:height,0:width/2]
	frameR=frame[0:height,width/2:width]

	imgL_pub.publish(bridge.cv2_to_imgmsg(frameL, "bgr8"))
	imgR_pub.publish(bridge.cv2_to_imgmsg(frameR, "bgr8"))

	cv2.imshow("frame", cv2.resize(frameL, (0,0), fx=0.1, fy=0.1))
	fps.update()

	k=cv2.waitKey(1)
	if k== 27:
		break
