#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String
from ghattas_vision.msg import vision_target,vision_task_detection
from imutils.video import VideoStream
from mode_selector import mode_selector
from cycle import cycle
from FPS import FPS

topics={'gate','path','bouy','torpedo','dropper'}
class vision_node(object):

    def __init__(self):
        rospy.init_node("vision_node")
        self._stream = VideoStream(src='/home/ahmad/catkin_ws/src/ghattas_vision/test_media/gate_animation.mkv').start()
        self._fps = FPS()
        self._target_out=vision_target()
        self._detection_out=vision_task_detection()
        self._mode_config = mode_selector('full')
        self._frame = None
        self._drawn = None
        self._publishers={}
        self._publishers['detection'] = rospy.Publisher('vision/detection', vision_task_detection, queue_size=10, latch=True)
        for topic in topics:
            self._publishers[topic] = rospy.Publisher('vision/'+topic, vision_target, queue_size=10, latch=True)
        self._subscriber = rospy.Subscriber("vision/mode", String, self.mode_change)

    def mode_change(self,mode):
        self._mode_config = mode_selector(mode.data)

    def _publish(self,topic,msg):
        self._publishers[topic].publish(msg)

    def _reset_target_msg(self):
        self._target_out=vision_target()

    def _reset_detection_msg(self):
        self._detection_out=vision_task_detection()


if __name__ == "__main__":
    vision = vision_node()
    rospy.loginfo(vision._mode_config)

    while True:
        vision._frame = vision._stream.read()
        vision._drawn = vision._frame
        vision._reset_detection_msg()

        if vision._frame is None:
            print('video feed is lost :(')
            cv2.waitKey(0)
            break
        vision._frame=cv2.resize(vision._frame, (0,0), fx=0.25, fy=0.25)
        vision._drawn=cv2.resize(vision._drawn, (0,0), fx=0.25, fy=0.25)
        cycle(vision)
        vision._publish('detection',vision._detection_out)
        cv2.imshow('frame',vision._frame)
        cv2.imshow('drawn',vision._drawn)
        vision._fps.update()
        #rospy.sleep(0.05)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    vision._stream.stop()
