#!/usr/bin/env python
import rospy
import cv2

from std_msgs.msg import String
from ghattas_vision.msg import vision_target,vision_task_detection
from _classes.task_class import task_class

from imutils.video import VideoStream
from cycle import cycle
from _utils.FPS import FPS
from _utils.manual_select import manual_select
from _utils.screen_grab import screen_grab

class vision_node(object):

    def __init__(self,src):
        rospy.init_node("vision_node")
        self._stream = VideoStream(src=src).start()
        self._fps = FPS()
        self._msg=vision_task_detection()
        self._frame = None
        self._drawn = None
        self._publisher = rospy.Publisher('vision/detection', vision_task_detection, queue_size=10, latch=True)

    def _publish(self):
        self._publisher.publish(self._msg)

    def _reset_msg(self):
        self._msg=vision_task_detection()

    def _read_frame(self):
        self._frame = self._stream.read()
        #vision._frame=cv2.resize(vision._frame, (0,0), fx=0.25, fy=0.25)
        self._drawn = self._frame.copy()


if __name__ == "__main__":
    vision = vision_node(0)
    tasks={}
    for task in {'gate','path','bouy','torpedo','dropper'}:
        tasks[task] = task_class(task)

    area = {'top': 50, 'left': 0, 'width': 800, 'height': 600}

    while True:
        #vision._read_frame()
        vision._reset_msg()
        #for simulation and to grab screen or an area of the screen uncomment below
        vision._frame = screen_grab(area)
        vision._frame = cv2.cvtColor(vision._frame, cv2.COLOR_BGRA2BGR)
        vision._drawn = vision._frame.copy()

        if vision._frame is None:
            print('video feed is lost :(')
            cv2.waitKey(0)
            break


        cycle(vision, tasks)

        vision._publish()

        cv2.imshow('frame',vision._frame)
        cv2.imshow('drawn',vision._drawn)
        vision._fps.update()

        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        else:
            manual_select(k, tasks, vision._frame)

    cv2.destroyAllWindows()
    vision._stream.stop()
