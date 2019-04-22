#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from std_srvs.srv import Empty, EmptyResponse


class save_hdg(object):

    def __init__(self):
        self.init_hdg()
        self.latch_publisher = rospy.Publisher('/autonomous/saved_heading',
                                               Float64,queue_size=10,latch=True)
        self.serv = rospy.Service('/autonomous/save_heading',Empty, self.publish_once_only)
        self.hdg_subscriber = rospy.Subscriber('/mavros/global_position/compass_hdg', Float64,
                                               self.subscriber_callback, queue_size=1)
        self.rate = rospy.Rate (10)
        self.initialize_topic()
        rospy.loginfo("The save heading service is ready")

    #Since the topic wont exist for the first time it should be initialized with any value
    def initialize_topic(self):
        init_msg = Float64()
        init_msg.data = 0.0
        self.latch_publisher.publish(init_msg)

    def init_hdg(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/global_position/compass_hdg",
                                                   Float64, timeout=1)
            except:
                rospy.loginfo("/compass_hdg topic is not ready yet, retrying")

        rospy.loginfo("/compass_hdg topic READY")

    def publish_once_only(self,req):
        rospy.loginfo("save heading service has been called")
        self.hdg = self.current_heading
        try:
            self.latch_publisher.publish(self.hdg)
            rospy.loginfo("Published")
            self.rate.sleep()
        except rospy.ROSInterruptException:
            raise e

    def subscriber_callback(self,msg):
        self.current_heading = msg.data

if __name__ == "__main__":
    rospy.init_node("save_heading")
    save_heading_object = save_hdg()
    rospy.spin()
