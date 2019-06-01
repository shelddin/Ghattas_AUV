#!/usr/bin/env python

## this code is to convert the twist velocities into suitable values for mavros RC_channels
import rospy
from mavros_msgs.msg import OverrideRCIn
from geometry_msgs.msg import Twist

class twist_to_thrusters(object):

    def __init__(self):
        self.control_msg_pub = rospy.Publisher('/autonomous/control_msg', OverrideRCIn,queue_size=10, latch = True)
        self.twist_sub = rospy.Subscriber('/mobile_base/commands/velocity', Twist,self.callback, queue_size =10)
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.twist_forward_max = rospy.get_param("max_vel_x")
        self.twist_forward_min = rospy.get_param("min_vel_x")
        self.twist_turn_max = rospy.get_param("max_vel_theta")
        self.twist_turn_min = rospy.get_param("min_in_place_vel_theta")
        self.thrust_forward_max = rospy.get_param("thrust_forward_max")
        self.thrust_forward_min = rospy.get_param("thrust_forward_min")
        self.thrust_turnr_max = rospy.get_param("thrust_turnr_max")
        self.thrust_turnr_min = rospy.get_param("thrust_turnr_min")
        self.thrust_turnl_max = rospy.get_param("thrust_turnl_max")
        self.thrust_turnl_min = rospy.get_param("thrust_turnl_min")
        self.override_msg = OverrideRCIn()


    def callback(self,msg):
        self.override_msg.channels = [1500 for x in range(len(self.override_msg.channels))]
        if msg.linear.x == 0:
            self.override_msg.channels[4] = 1500
        else:
            self.override_msg.channels[4] = self.convert_range(msg.linear.x,'f')

        if msg.angular.z == 0:
            self.override_msg.channerls[3] = 1500
        elif msg.angular.z > 0 :
            self.override_msg.channels[3] = self.convert_range(msg.angular.z,'rr')
        elif msg.angular.z < 0 :
            self.override_msg.channels[3] = self.convert_range(abs(msg.angular.z),'rl')

        self.control_msg_pub.publish(self.override_msg)
        self.rate.sleep()



    def convert_range (self,value,mode):

        if mode == 'f':
            old_max = self.twist_forward_max
            old_min = self.twist_forward_min
            new_max = self.thrust_forward_max
            new_min = self.thrust_forward_min

        elif mode == 'rr':
            old_max = self.twist_turn_max
            old_min = self.twist_turn_min
            new_max = self.thrust_turnr_max
            new_min = self.thrust_turnr_min

        elif mode == 'rl':
            old_max = self.twist_turn_max
            old_min = self.twist_turn_min
            new_max = self.thrust_turnl_max
            new_min = self.thrust_turnl_min

        old_value = value
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
        return new_value

if __name__ == '__main__':
    rospy.init_node('twist_to_thrusters')
    object__ = twist_to_thrusters()
    rospy.spin()
