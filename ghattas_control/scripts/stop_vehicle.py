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
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10) # Publisher object
        self.service_server_object = rospy.Service('/autonomous/stop_vehicle',
                                                   Empty, self.service_callback) # service server object
        self.stop_condition = rospy.Publisher('/autonomous/stopped',Bool,queue_size=10,latch = True) # publisher object
        rospy.loginfo("The stop_vehicle service is ready ") # logging some info
        self.initialize_topic()
        self.rate = rospy.Rate (10) # initiaing the publishing rate to be used

    #Since the topic wont exist for the first time it should be initialized with any value
    def initialize_topic(self):
        init_msg = Bool()
        init_msg.data = True
        self.stop_condition.publish(init_msg)

    # a method which will publish only once in the required topic
    def publish_once_only(self,status):
        try:
            self.stop_condition.publish(status)
            rospy.loginfo("Published a %s stop status",status)
            self.rate.sleep()
        except rospy.ROSInterruptException:
            raise e

        return EmptyResponse()


    #The service call back where your service will execute this method whenever you call it
    def service_callback(self,req):
        rospy.loginfo("vehicle stopping ...")
        override_msg = OverrideRCIn()
        override_msg.channels = [1500 for x in range(len(override_msg.channels))]
        self.rc_publisher.publish(override_msg)
        self.publish_once_only(True)
        self.rate.sleep()
        rospy.loginfo("vehicle Stopped")
        return EmptyResponse()


#The main loop to run the whole code
if __name__ == '__main__':
    rospy.init_node('stop_vehicle') # initiatint a ros node with a unique name in the system
    object__ = stop_vehicle() # object of our class
    rospy.spin() # we call this always so the code will be running infinitly
