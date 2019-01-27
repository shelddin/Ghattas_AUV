#!/usr/bin/env python

"""
## ------- code functionaliy -------------##
to move the vehicle non-stop in all directions untill a stop service is called or command to other direction
the list of commands are l,r,f,b,rl,rr,u,d
l = sway left
r = sway right
f = surge forward
b = surge backward
rl = rotate left
rr = rotate right
u = go up
d = go down
"""

# importing all necessary modules
import sys
import rospy
import time

#importing the necessary ROS msgs and srvs
from ghattas_control_advanced.srv import move, moveResponse
from std_msgs.msg import Float64
from std_msgs.msg import Bool
from mavros_msgs.msg import OverrideRCIn


# the main class for the service server
class mover(object):
    def __init__(self): # constructor
        # publiser object to publish in '/mavros/rc/override' to move the vehicle
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        # service object to start out service server
        self.service_server_object = rospy.Service('/autonomous/move', move, self.service_callback)

        # getting all the parameters from the parameter server and stor it in variables
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
        rospy.loginfo("The move service is ready ") # debug msg

    # service callback the functionality to be done when the service is called
    def service_callback(self, req):
        # dictionary to store the index of channel to control the vehicle
        # as indicated on the ArduSub website
        index = {'l':5,'r':5,'f':4,'b':4,'rl':3,'rr':3,'u':2,'d':2}
        # dictionary for easy access to the speeds values
        speed = {'l':self.left_sway_speed,'r':self.right_sway_speed,'f':self.forward_speed,
                    'b':self.backward_speed,'rl':self.left_rotation_speed,'rr':self.right_rotation_speed,
                    'u':self.up_speed,'d':self.down_speed}
        loginfo_msg = {'l':"lateral left",'r':"lateral right",'f':"forward",'b':"backward",'rl':"left roatation",
                        'rr':"right rotation",'u':"depth up",'d':"depth down"}

        override_msg = OverrideRCIn() #object of the msg type for the RC
        if req.direction in index: #error catcher to verify a valid direction is sent
            override_msg.channels[index[req.direction]] = speed[req.direction]
            self.rc_publisher.publish(override_msg)
            self.rate.sleep()
            rospy.loginfo("The vehicle started doing a %s",loginfo_msg[req.direction])
            return True
        else: #catching the error
            rospy.logerr("you have endered wrong direction for move service")

if __name__ == '__main__': # main funciton
    rospy.init_node('move_serviceServer') # initiaing a ros node
    object__ = mover() # object of the main class
    rospy.spin() # to ensure the the code will run inifinitly
