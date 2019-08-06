#!/usr/bin/env python

import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Joy

class joystick(object):
    def __init__(self):
        self.open_pub = rospy.Publisher('arduino/open_gripper', Empty, queue_size=10)
        self.close_pub = rospy.Publisher('arduino/close_gripper', Empty, queue_size=10)
        self.light_inc_pub = rospy.Publisher('arduino/light_inc',Empty, queue_size=10)
        self.light_dec_pub = rospy.Publisher('arduino/light_dec',Empty, queue_size=10)
        self.torpedo_pub = rospy.Publisher('arduino/launch_torpedo', Empty, queue_size=10)
        self.dropper_pub = rospy.Publisher('arduino/open_dropper', Empty, queue_size=10)
        self.JoySub = rospy.Subscriber('joy',Joy,self.callback,queue_size=1)
        self.valid_js_channels = [7,5,9,8,10,0] # channels to be used from the joystick
        self.publishers = {7:self.open_pub,5:self.close_pub,9:self.light_inc_pub,8:self.light_dec_pub,10:self.torpedo_pub,0:self.dropper_pub} # linking js channels with publisher
        self.pmsg = Empty()
        self.rate = rospy.Rate(10) # 10hz
        rospy.loginfo("ROV mode ready")

    def callback (self,msg):

        if 1 in msg.buttons and msg.buttons.index(1) in self.valid_js_channels:
            self.publishers[msg.buttons.index(1)].publish(self.pmsg)
            self.rate.sleep()
            rospy.loginfo("empty msg sent")


if __name__ == '__main__':
    rospy.init_node("joystick")
    object = joystick()
    rospy.spin()
