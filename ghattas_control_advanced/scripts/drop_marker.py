#!/usr/bin/env python


"""
## ------- code functionaliy -------------##

"""
import rospy
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Bool

class drop_marker (object):

    def __init__(self):
        self.drop_state = Bool()
        self.drop = rospy.Publisher("/drop_marker_state",Bool,queue_size=10,latch = True)
        self.serv = rospy.Service("/drop_marker",Empty,self.publish_once_only)
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.initialize_topic()
        rospy.loginfo("The drop marker service is ready")

    def initialize_topic(self):
        init_msg = Bool()
        init_msg.data = False
        self.drop.publish(init_msg)

    def publish_once_only(self,req):
        rospy.loginfo("drop marker service has been called")
        try:
            rospy.loginfo("dropping the marker ...")
            self.drop.publish(True)
            rospy.loginfo("marker dropped")
            self.rate.sleep()
        except rospy.ROSInterruptException:
            raise e

if __name__ == "__main__":
    rospy.init_node("drop_marker")
    save_heading_object = drop_marker()
    rospy.spin()
