#!/usr/bin/env python
import sys
import rospy
import time
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from mavros_msgs.msg import OverrideRCIn

# the list of commands are l,r,f,b,rl,rr,u,d
class move(object):
    def __init__(self):
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        self.service_server_object = rospy.Service('/autonomous/move', Empty, self.service_callback)
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.forward_speed = rospy.get_param("forward_speed")
        self.backward_speed = rospy.get_param("backward_speed")
        self.left_sway_speed = rospy.get_param("left_sway_speed")
        self.right_sway_speed = rospy.get_param("right_sway_speed")
        self.left_rotation_speed = rospy.get_param("left_rotation_speed")
        self.right_rotation_speed = rospy.get_param("right_rotation_speed")
        self.up_speed = rospy.get_param("up_speed")
        self.down_speed = rospy.get_param("down_speed")
        rospy.loginfo("The move service is ready ")


    def service_callback(self, req):
        index = {'l':5,'r':5,'f':4,'b':4,'rl':3,'rr':3,'u':2,'d':2}
        speed = {'l':self.left_sway_speed,'r':self.right_sway_speed,'f':self.forward_speed,
                    'b':self.backward_speed,'rl':self.left_rotation_speed,'rr':self.right_rotation_speed,
                    'u':self.up_speed,'d':self.down_speed}
        override_msg = OverrideRCIn()
        if req.direction in index:
            override_msg.channels[index[req.direction]] = speed[req.direction]
            self.rc_publisher.publish(override_msg)
            self.rate.sleep()
            stopped = self.get_stop_condition()
            return True
        else:
            rospy.logerr("you have endered wrong direction for move service")

if __name__ == '__main__':
    rospy.init_node('move_serviceServer')
    object__ = move()
    rospy.spin()
