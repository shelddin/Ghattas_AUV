#!/usr/bin/env python
import sys
import rospy
import time
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from mavros_msgs.msg import OverrideRCIn


class heave_down(object):
    def __init__(self):
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        self.service_server_object = rospy.Service('/autonomous/heave_down', Empty, self.service_callback)
        self.sub_stop_condition = rospy.Subscriber('/autonomous/stopped',Bool, self.sub_callback )
        self.pub_stop_condition = rospy.Publisher('/autonomous/stopped',Bool, queue_size=10, latch = True)
        rospy.loginfo("The heave_down service is ready ")
        self.rate = rospy.Rate(10)

    def sub_callback(self,msg):
        self.is_stop = msg

    #this our getter function for the stop condiditon
    def get_stop_condition(self):
        return self.is_stop.data

    # to make sure the vehicle is enabled for movement
    def _is_stop (self):
        self.pub_stop_condition.publish(False)
        return False

    def service_callback(self, req):
        rospy.loginfo("Going Down ...")
        stopped = self._is_stop()
        override_msg = OverrideRCIn()
        override_msg.channels[2] = 1400
        self.rc_publisher.publish(override_msg)
        self.rate.sleep()
        stopped = self.get_stop_condition()
        return EmptyResponse()

if __name__ == '__main__':
    rospy.init_node('surge_forward_serviceServer')
    object__ = heave_down()
    rospy.spin()
