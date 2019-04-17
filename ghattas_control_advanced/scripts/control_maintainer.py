#!/usr/bin/env python

"""
This code to maintain the connection between the companion computer and the Pixhawk and maintain continous RC Override msg
"""

# importing all necessary modules
import sys
import rospy
import time
from mavros_msgs.msg import OverrideRCIn

class control_msg_tools(object):

    def __init__(self):
        self.control_subscriber = rospy.Subscriber('/autonomous/control_msg', OverrideRCIn, self.callback, queue_size =1)
        self.chnage_flag = False
        self.current_control_msg = OverrideRCIn()
        self.current_control_msg.channels = [1500 for x in range(len(self.current_control_msg.channels))]
        rospy.loginfo("started the control maintainer")

    def callback (self,msg):
        self.changeflag = True
        self.current_control_msg = msg

class maintain (object):

    def __init__(self):
        self.rc_publisher = rospy.Publisher('/mavros/rc/override',OverrideRCIn, queue_size = 1)
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.tools_object = control_msg_tools()
        self.current_msg = self.tools_object.current_control_msg

    def run(self):
        while 1:
            self.current_msg = self.tools_object.current_control_msg
            self.rc_publisher.publish(self.current_msg)
            self.rate.sleep()

if __name__ == '__main__':
    rospy.init_node('control_maintainer')
    object__ = maintain()
    object__.run()
    rospy.spin()
