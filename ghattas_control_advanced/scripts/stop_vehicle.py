#!/usr/bin/env python

# importing the required modules
import sys
import rospy
import time

#importing the necessary srv types and msgs to communicate through ROS
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Float64
from mavros_msgs.msg import OverrideRCIn
from std_msgs.msg import Bool

class stop_vehicle(object):

    # The constructor of the class
    def __init__(self):
        self.control_msg_pub = rospy.Publisher('/autonomous/control_msg', OverrideRCIn,
                                            queue_size=10, latch = True) # Publisher object
        self.service_server_object = rospy.Service('/autonomous/stop_vehicle',
                                                   Empty, self.service_callback) # service server object
        rospy.loginfo("The stop_vehicle service is ready ") # logging some info
        self.rate = rospy.Rate (10) # initiaing the publishing rate to be used

    #The service call back where your service will execute this method whenever you call it
    def service_callback(self,req):
        rospy.loginfo("vehicle stopping ...")
        override_msg = OverrideRCIn()
        override_msg.channels = [1500 for x in range(len(override_msg.channels))]
        self.control_msg_pub.publish(override_msg)
        self.rate.sleep()
        rospy.loginfo("vehicle Stopped")
        return EmptyResponse()


#The main loop to run the whole code
if __name__ == '__main__':
    rospy.init_node('stop_vehicle') # initiatint a ros node with a unique name in the system
    object__ = stop_vehicle() # object of our class
    rospy.spin() # we call this always so the code will be running infinitly
