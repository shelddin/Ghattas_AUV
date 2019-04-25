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

class depth_control(object):

    def __init__(self):
        self.depth_tools_object = depth_tools()
        self.control_msg_pub = rospy.Publisher('/autonomous/control_msg', OverrideRCIn,
                                            queue_size=10, latch = True)
        self.service_server_object = rospy.Service('/autonomous/depth_control',
                                                   depth, self.service_callback)
        update_params()
        self.rate = rospy.Rate (self.pub_rate)
        rospy.loginfo("The depth control service is ready ")

    def update_params(self):
        self.down_speed = rospy.get_param("down_speed")
        self.up_speed = rospy.get_param("up_speed")
        self.pub_rate = rospy.get_param("pub_rate")

    def service_callback(self, req):
        current_depth = self.depth_tools_object.get_current_depth()
        goal_depth = req.desired_depth
        update_params()
        if goal_depth < current_depth: # means the direction is DOWN
            throttle_speed = self.down_speed
        elif goal_depth > current_depth: # means the direction is UP
            throttle_speed = self.up_speed
        rospy.loginfo("The vehicle started to heave_down to depth: %f",goal_depth)
        while(int(current_depth) != int(goal_depth)):
            current_depth = self.depth_tools_object.get_current_depth()
            override_msg = OverrideRCIn()
            override_msg.channels[2] = throttle_speed
            self.control_msg_pub.publish(override_msg)
            self.rate.sleep()
            current_depth = self.depth_tools_object.get_current_depth()
        override_msg.channels[2] = 1500
        self.control_msg_pub.publish(override_msg)
        self.rate.sleep()
        rospy.loginfo("The vehicle reached a depth of: %f successfully",self.depth_tools_object.get_current_depth())
        return True
if __name__ == '__main__':
    rospy.init_node('depth_control_serviceServer')
    object__ = depth_control()
    rospy.spin()
