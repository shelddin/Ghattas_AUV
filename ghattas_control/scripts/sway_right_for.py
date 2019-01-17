#!/usr/bin/env python
import math
import rospy
from ghattas_control.srv import dist, distResponse
from mavros_msgs.msg import OverrideRCIn
from nav_msgs.msg import Odometry

#### The movement is NOT ACCURATE
#+ Line

class dist_tools (object):

    def __init__ (self):
        self.init_odom()
        self.hdg_subscriber = rospy.Subscriber("/mavros/local_position/odom",Odometry,
                                               self.coordinates_callback,queue_size=1)
    def init_odom(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/local_position/odom",
                                                   Odometry, timeout=1)
            except:
                rospy.loginfo("/odom topic is not ready yet, retrying")

        rospy.loginfo("/odom topic READY")

    def coordinates_callback(self,msg):
        self.current_x_coor = msg.pose.pose.position.x
        self.current_y_coor = msg.pose.pose.position.y

    def get_coor(self):
        current_corr = [self.current_x_coor,self.current_y_coor]
        return current_corr

class sway_right_for(object):

    def __init__(self):

        self._dist_tools = dist_tools()
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        self.service_server_object = rospy.Service('/autonomous/sway_right_for',
                                                   dist, self.service_callback)
        rospy.loginfo("The sway_right_for service is ready ")
        self.rate = rospy.Rate (10)

    def calc_distance(self,coor1,coor2):
        distance = math.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
        return distance

    def service_callback(self,req):
        location1 = self._dist_tools.get_coor()
        override_msg = OverrideRCIn()
        goal_distance = req.desired_distance
        current_distance = 0
        while (goal_distance != int(current_distance)):
            override_msg.channels[5] = 1800
            self.rc_publisher.publish(override_msg)
            self.rate.sleep()
            location2 = self._dist_tools.get_coor()
            current_distance = self.calc_distance(location1,location2)
        override_msg.channels[5] = 1500
        self.rc_publisher.publish(override_msg)
        self.rate.sleep()
        rospy.loginfo("The vehicle travelled a distance of: %f successfully",current_distance)
        return True

if __name__ == '__main__':

    rospy.init_node('sway_right_for_serviceServer')
    object__ = sway_right_for()
    rospy.spin()
