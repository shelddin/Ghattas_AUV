#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse
from ghattas_control.msg import vehicle_state
from nav_msgs.msg import Odometry


class save_state(object):

    def __init__(self):
        self.init_hdg()
        self.latch_publisher = rospy.Publisher('/autonomous/saved_vehicle_state',
                                               vehicle_state,queue_size=10,latch=True)

        self.hdg_subscriber = rospy.Subscriber('/mavros/global_position/compass_hdg', Float64,
                                               self.hdg_callback, queue_size=1)
        self.depth_subscriber = rospy.Subscriber("/mavros/global_position/rel_alt",Float64,
                                               self.depth_callback,queue_size=1)
        self.hdg_subscriber = rospy.Subscriber("/odom",Odometry,
                                               self.pose_callback,queue_size=1)
        self.rate = rospy.Rate (10)
        self.serv = rospy.Service('/autonomous/save_vehicle_state',Empty, self.save)
        self.initialize_topic()
        rospy.loginfo("The save state service is ready")

    def initialize_topic(self):
        init_msg = vehicle_state()
        init_msg.depth = 0.0
        init_msg.heading = 0.0
        init_msg.pitch = 0.0
        init_msg.position.x = 0.0
        init_msg.position.y = 0.0
        init_msg.position.z = 0.0
        self.latch_publisher.publish(init_msg)

    def depth_callback(self, msg):
        self._depth = msg
    def hdg_callback(self, msg):
        self._hdg = msg
    def pose_callback(self, msg):
        self._x = msg.pose.pose.pose.position.x
        self._y = msg.pose.pose.pose.position.y
        self._z = msg.pose.pose.pose.position.z
    #Since the topic wont exist for the first time it should be initialized with any value

    def save(self,req):
        rospy.loginfo("save vehicle state service has been called")
        self.state_msg = vehicle_state()
        self.state_msg.depth = self._depth
        self.state_msg.heading = self._hdg
        self.state_msg.pose.x = self._x
        self.state_msg.pose.y = self._y
        self.state_msg.pose.z = self._z
        try:
            self.latch_publisher.publish(self.state_msg)
            rospy.loginfo("saved new vehicle state")
            self.rate.sleep()
        except rospy.ROSInterruptException:
            raise e

if __name__ == "__main__":
    rospy.init_node("save_vehicle_state")
    save_heading_object = save_state()
    rospy.spin()
