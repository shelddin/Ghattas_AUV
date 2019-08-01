#!/usr/bin/env python

import sys
import rospy
from ghattas_control.srv import depth_adv, depth_advResponse, depth_advRequest
from ghattas_navigation.srv import vehicle_state, vehicle_stateResponse, vehicle_stateRequest
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

class navigation(object):

    def __init__(self):

        self.move_base_client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.move_base_client.wait_for_server()
        rospy.wait_for_service('/autonomous/depth_control')
        self.depth_client = rospy.ServiceProxy('/autonomous/depth_control',depth_adv)
        rospy.wait_for_service('/autonomous/heading_control')
        self.heading_client = rospy.SerivceProxy('/autonomous/heading_control', hdg_adv)
        self.navigation_server = rospy.Service('/autonomous/navigation',vehicle_state, self.callback)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.subcallback)
        rospy.loginfo("navigation service is ready")


    def callback(self ,req):

        try:
            self.depth_client(req.pose.position.z + self.current_pose.pose.pose.position.z)
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = "map"
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = req.pose.position.x + self.current_pose.pose.pose.position.x
            goal.target_pose.pose.position.y = req.pose.position.y + self.current_pose.pose.pose.position.y
            goal.target_pose.pose.orientation.w = 1.0
            self.move_base_client.send_goal(goal)
            wait = self.move_base_client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                return self.move_base_client.get_result()

        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")

            self.heading_control(req.heading)

    def subcallback(self, msg):
        self.current_pose = msg

if __name__=='__main__':
    rospy.init_node('navigation_node')
    opject__ = navigation()
    rospy.spin()
