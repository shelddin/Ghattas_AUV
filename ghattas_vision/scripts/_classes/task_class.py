import cv2
import rospy
from ghattas_vision.msg import vision_target
from _processing.perspective_solve import pnp
from _param.task_param import world_pts,colors


class task_class(object):
    """docstring for task."""
    def __init__(self, name):
        super(task_class, self).__init__()
        rospy.init_node("vision_node")
        self._name = name
        self._publisher = rospy.Publisher('/vision/'+ self._name, vision_target, queue_size=10, latch=True)
        self._world_pts = world_pts[self._name]
        self._msg = vision_target()
        self._bbox = None
        self._detection_state = False
        self._tracker = cv2.TrackerMedianFlow_create()
        self._colors = colors[self._name]

    def _pub(self):
        self._msg_gen()
        self._publisher.publish(self._msg)

    def _msg_gen(self):
        self._reset_msg()
        self._msg.found = self._detection_state
        self._msg.x = (self._bbox.x+self._bbox.w)/2
        self._msg.y = (self._bbox.y+self._bbox.h)/2

    def _reset_msg(self):
        self._msg=vision_target()

    def _pnp(self, frame):
        success, rotation_vector, translation_vector = pnp(frame, self._bbox, self._world_pts)

    def _detected(self, frame, bbox):
        self._bbox = bbox
        self._detection_state = self._tracker.init(frame, self._bbox)
        print(self._detection_state)

    def _track(self, frame):
        if self._detection_state:
            self._detection_state, self._bbox = self._tracker.update(frame)
        else:
            pass
