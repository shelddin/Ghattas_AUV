#!/usr/bin/env python
import sys
import rospy
import time
from ghattas_control.srv import depth, depthResponse
from std_msgs.msg import Float64
from mavros_msgs.msg import OverrideRCIn


class depth_tools(object):
    def __init__(self):
        self.init_hdg()
        self.hdg_subscriber = rospy.Subscriber("/mavros/global_position/rel_alt",Float64,
                                               self.depth_callback,queue_size=1)
    def init_hdg(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/global_position/rel_alt",
                                                   Float64, timeout=1)
            except:
                rospy.loginfo("/rel_alt topic is not ready yet, retrying")

        rospy.loginfo("/rel_alt topic READY")

    def depth_callback(self, msg):
        self._depth = msg
    def get_current_depth(self):
        return self._depth.data

class heave_up(object):
    def __init__(self):
        self.depth_tools_object = depth_tools()
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        self.service_server_object = rospy.Service('/autonomous/heave_up_to',
                                                   depth, self.service_callback)
        rospy.loginfo("The heave_up service is ready ")
        self.rate = rospy.Rate (10)

    def service_callback(self, req):
        current_depth = self.depth_tools_object.get_current_depth()
        goal_depth = req.desired_depth
        rospy.loginfo("The vehicle started to heave_up to depth: %f",goal_depth)

        while(current_depth < goal_depth):
            current_depth = self.depth_tools_object.get_current_depth()
            override_msg = OverrideRCIn()
            override_msg.channels[2] = 1600
            self.rc_publisher.publish(override_msg)
            self.rate.sleep()
            current_depth = self.depth_tools_object.get_current_depth()
        override_msg.channels[2] = 1500
        self.rc_publisher.publish(override_msg)
        self.rate.sleep()
        rospy.loginfo("The vehicle reached a depth of: %f successfully",self.depth_tools_object.get_current_depth())
        return True


if __name__ == '__main__':
    rospy.init_node('heave_up_to_serviceServer')
    object__ = heave_up()
    rospy.spin()
