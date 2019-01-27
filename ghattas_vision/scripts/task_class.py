import cv2
import rospy
from ghattas_vision.msg import vision_target
from perspective_solve import pnp
from param import world_pts


class task(object):
    """docstring for task."""
    def __init__(self, node, name):
        super(task, self).__init__()
        self._node = node
        self._name = name
        self._publisher = rospy.Publisher('/vision/'+ self._name, vision_target, queue_size=10, latch=True)
        self._world_pts = world_pts[self._name]
        self._msg = vision_target()
        self._bbox = None
        self._detection_state = False
        self._tracker = cv2.TrackerGOTURN_create()

    def pub(self):
        self.msg_gen()
        self._publisher.publish(self._msg)

    def msg_gen(self):
        self._msg.found = self._detection_state
        self._msg.x = self._bbox.x
        self._msg.y = self._bbox.y

    def pnp(self, frame):
        success, rotation_vector, translation_vector = pnp(node._frame, self._bbox, self._world_pts)

    def detected(self, frame, bbox):
        self._bbox = bbox
        self._detection_state = self._tracker.init(node._frame, self._bbox)

    def track(self, frame):
        self._detection_state, self._bbox = self._tracker.update(node._frame)
