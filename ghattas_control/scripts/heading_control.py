#!/usr/bin/env python

"""
## ------- IMPORTANT NOTE -------------##
## can be Improved by using only one for rotation not if statement
"""

# Importing all neccessary libraries to be used
import rospy # the official ROS library for python programming
from ghattas_control_advanced.srv import hdg_adv, hdg_advResponse # custom srv type defined in the same package here
from std_msgs.msg import Float64 # standard msg type from ROS
from mavros_msgs.msg import OverrideRCIn # msg type for MAVROS package to send RC commands

# This class to retrieve the msgs in "mavros/global_position/compass_hdg" and "/autonomous/saved_heading"
# details about the topics below
class hdg_tools(object):
    def __init__(self): # constructor
        self.init_hdg() #function call
        #Subscriber object to "/mavros/global_position/compass_hdg" which prvide the current heading of the vehicle
        self.hdg_subscriber = rospy.Subscriber("/mavros/global_position/compass_hdg",Float64,
                                               self.hdg_callback,queue_size=1)
        #Subscriber object to "/autonomous/saved_heading" which contain the saved heading from previous mission
        self.save_subscriber = rospy.Subscriber("/autonomous/saved_heading", Float64,
                                                self.saved_callback,queue_size=10)

    # this function checks whether the topic is available or not!
    def init_hdg(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/global_position/compass_hdg",
                                                   Float64, timeout=1)
            except:
                rospy.loginfo("/compass_hdg topic is not ready yet, retrying")

        rospy.loginfo("/compass_hdg topic READY")

    # subscriber call back
    def hdg_callback(self, msg):
        self._heading = msg
    # getter function
    def get_current_hdg(self):
        return self._heading.data
    # subscriber call back
    def saved_callback(self, msg):
        self._saved_heading = msg
    # getter function
    def get_saved_heading (self):
        return self._saved_heading.data


class heading_accurate_movement (object):

    def __init__(self):
        self.hdg_tools_object = hdg_tools()
        self.control_msg_pub = rospy.Publisher('/autonomous/control_msg', OverrideRCIn,
                                            queue_size=10, latch = True)
        self.service_server_object = rospy.Service('/autonomous/heading_control',
                                                   hdg_adv, self.service_callback)

        update_params()
        self.rate = rospy.Rate (self.pub_rate)

        rospy.loginfo("Heading control service is ready")

    def update_params(self):
        self.right_rotation_speed = rospy.get_param("right_rotation_speed")
        self.left_rotation_speed = rospy.get_param("left_rotation_speed")
        self.pub_rate = rospy.get_param("pub_rate")

    def service_callback(self, req):

        if req.mode == 'ht':
            goal_heading = req.desired_hdg
        elif req.mode == 'hts':
            goal_heading = self.hdg_tools_object.get_saved_heading()
        else:
            rospy.logerr("You have entered wrong mode for heading control service")
        update_params()
        current_heading = self.hdg_tools_object.get_current_hdg()
        direction = self.shortest_path(goal_heading)
        override_msg = OverrideRCIn()
        if direction == 'r': #rotating to the Right
        #using the 4th cannel and a value above 1500
        #rospy.loginfo("the current heading is {}",format(current_heading))
            rospy.loginfo("Rotating to the right")
            while (int(current_heading) != int(goal_heading)):
                override_msg.channels[3] = self.right_rotation_speed
                self.control_msg_pub.publish(override_msg)
                self.rate.sleep()
                current_heading = self.hdg_tools_object.get_current_hdg()
            override_msg.channels[3] = 1500
            self.control_msg_pub.publish(override_msg)
            self.rate.sleep()
            rospy.loginfo("Stopped rotating heading reached : %f",self.hdg_tools_object.get_current_hdg())
            return True
        elif direction == 'l':  #rotating to the left
        # using the 4 channel and value below 1500
            rospy.loginfo("rotating to the left")
            while (int(current_heading) != int(goal_heading)):
                override_msg.channels[3] = self.left_rotation_speed
                self.control_msg_pub.publish(override_msg)
                self.rate.sleep()
                current_heading = self.hdg_tools_object.get_current_hdg()

            override_msg.channels[3] = 1500
            self.control_msg_pub.publish(override_msg)
            self.rate.sleep()
            rospy.loginfo("Stopped rotating heading reached : %f",current_heading)
            return True
        else:
            rospy.logerr("The service did not work properly something went wrong")
            return False

    def shortest_path(self, goal_hdg):
        current_heading = self.hdg_tools_object.get_current_hdg()
        # To calculate the shortest path I divided the heading into 4 quarters and the
        #Algorithm as following
        if current_heading > goal_hdg:
            if 1 < goal_hdg < 90:
                return 'r'
            else:
                return 'l'
        elif current_heading < goal_hdg:
            if  270 < goal_hdg < 359:
                return 'l'
            else:
                return 'r'
        else:
            rospy.logerr("The goal heading value is not correct")
            rospy.logerr("The value should be between 0 - 360 or -1 ")

if __name__ == '__main__':
    rospy.init_node('heading_to_serviceServer')
    object__ = heading_accurate_movement()
    rospy.spin()
