#!/usr/bin/env python
import math
import rospy
from ghattas_control_advanced.srv import dist, distResponse
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

class long_lat_control(object):

    def __init__(self):

        self._dist_tools = dist_tools()
        self.rc_publisher = rospy.Publisher('/mavros/rc/override', OverrideRCIn,
                                            queue_size=10)
        self.service_server_object = rospy.Service('/autonomous/sway_right_for',
                                                   dist, self.service_callback)

        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.forward_speed = rospy.get_param("forward_speed")
        self.backward_speed = rospy.get_param("backward_speed")
        self.left_sway_speed = rospy.get_param("left_sway_speed")
        self.right_sway_speed = rospy.get_param("right_sway_speed")
        rospy.loginfo("The long_lat_control service is ready ")


    def calc_distance(self,coor1,coor2):
        distance = math.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
        return distance

    def service_callback(self,req):
        index = {'l':5,'r':5,'f':4,'b':4}
        speed = {'l':self.left_sway_speed,'r':self.right_sway_speed,'f':self.forward_speed,
                    'b':self.backward_speed}
        location1 = self._dist_tools.get_coor()
        override_msg = OverrideRCIn()
        goal_distance = req.desired_distance
        current_distance = 0
        while (goal_distance != int(current_distance)):
            override_msg.channels[index[req.direction]] = speed[req.direction]
            self.rc_publisher.publish(override_msg)
            self.rate.sleep()
            location2 = self._dist_tools.get_coor()
            current_distance = self.calc_distance(location1,location2)
        override_msg.channels[index[req.direction]] = 1500
        self.rc_publisher.publish(override_msg)
        self.rate.sleep()
        location2 = self._dist_tools.get_coor() # to get the
        rospy.loginfo("The vehicle travelled a distance of: %f successfully",self.calc_distance(location1,location2))
        return True

if __name__ == '__main__':
    rospy.init_node('long_lat_control_serviceServer')
    object__ = long_lat_control()
    rospy.spin()
