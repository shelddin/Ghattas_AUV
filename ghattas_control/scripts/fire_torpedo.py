#!/usr/bin/env python


"""
## ------- code functionaliy -------------##
this code to fire the torpedos by publishing the firing state to a topic which Arduino will subscribe to
"""
import rospy
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Bool

class fire_torpedo (object):

    def __init__(self):
        self.fire_state = Bool()
        self.fire = rospy.Publisher("/fire_torpedo_state",Bool,queue_size=10,latch = True)
        self.serv = rospy.Service("/fire_torpedo",Empty,self.publish_once_only)
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.initialize_topic()
        rospy.loginfo("The firing torpedo service is ready")

    def initialize_topic(self):
        init_msg = Bool()
        init_msg.data = False
        self.fire.publish(init_msg)

    def publish_once_only(self,req):
        rospy.loginfo("fire torpedo service has been called")
        try:
            rospy.loginfo("firing the Torpdeo ...")
            self.fire.publish(True)
            rospy.loginfo("Torpedo Fired")
            self.rate.sleep()
        except rospy.ROSInterruptException:
            raise e

if __name__ == "__main__":
    rospy.init_node("fire_torpedo")
    save_heading_object = fire_torpedo()
    rospy.spin()
