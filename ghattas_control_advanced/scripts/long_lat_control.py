#!/usr/bin/env python


"""
## ------- code functionaliy -------------##
to move the vehicle longitudally and laterally with an accurate movement with a pre-set distance value
"""
# imprting the neccessary modules
import math
import rospy

#importing the neccessary ROS msgs and srvs
from ghattas_control_advanced.srv import dist, distResponse
from mavros_msgs.msg import OverrideRCIn
from nav_msgs.msg import Odometry

#### The movement is NOT ACCURATE
#+ Line

# class to retrieve the current position of the vehicle
class dist_tools (object):

    def __init__ (self): #constructor
        self.init_odom() #function call

        #subscriber for the topic resposible of the current position
        self.hdg_subscriber = rospy.Subscriber("/mavros/local_position/odom",Odometry,
                                               self.coordinates_callback,queue_size=1)
    # funciton to check whether topic is available?
    def init_odom(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/local_position/odom",
                                                   Odometry, timeout=1)
            except:
                rospy.loginfo("/odom topic is not ready yet, retrying")

        rospy.loginfo("/odom topic READY")
    # callback function for the subscriber
    def coordinates_callback(self,msg):
        self.current_x_coor = msg.pose.pose.position.x
        self.current_y_coor = msg.pose.pose.position.y

    # getter function
    def get_coor(self):
        current_corr = [self.current_x_coor,self.current_y_coor]
        return current_corr

# main class for the service server
class long_lat_control(object):

    def __init__(self): #constructor

        self._dist_tools = dist_tools() #object of the tools class to get the data in this class
        self.control_msg_pub = rospy.Publisher('/autonomous/control_msg', OverrideRCIn,
                                            queue_size=10, latch = True)

        # service object to start out service server
        self.service_server_object = rospy.Service('/autonomous/precise_movement',
                                                   dist, self.service_callback)

        # getting all the parameters from the parameter server and stor it in variables
        self.pub_rate = rospy.get_param("pub_rate")
        self.rate = rospy.Rate (self.pub_rate)
        self.forward_speed = rospy.get_param("forward_speed")
        self.backward_speed = rospy.get_param("backward_speed")
        self.left_sway_speed = rospy.get_param("left_sway_speed")
        self.right_sway_speed = rospy.get_param("right_sway_speed")

        rospy.loginfo("The long_lat_control service is ready ")

    # function to calculate the distance between the start point and the current position
    def calc_distance(self,coor1,coor2):
        distance = math.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
        return distance
    # service callback the functionality to be done when the service is called
    def service_callback(self,req):

        # dictionary to store the index of channel to control the vehicle
        # as indicated on the ArduSub website
        index = {'l':5,'r':5,'f':4,'b':4}

        # dictionary for easy access to the speeds values
        speed = {'l':self.left_sway_speed,'r':self.right_sway_speed,'f':self.forward_speed,
                    'b':self.backward_speed}

        location1 = self._dist_tools.get_coor() # storing the start pos of the vehicle
        override_msg = OverrideRCIn() #object of the msg type for the RC
        goal_distance = req.desired_distance #getting the service request a
        current_distance = 0 #initiating the distance with 0 to avoid errors

        # moving the vehicle untill it travel the required distance
        while (goal_distance != int(current_distance)):
            override_msg.channels[index[req.direction]] = speed[req.direction] #setting the speed to the correct RC channel
            self.control_msg_pub.publish(override_msg) # publishing the msg to start movement
            self.rate.sleep() # making sure to have the same publish rate
            location2 = self._dist_tools.get_coor() # update the current location
            current_distance = self.calc_distance(location1,location2) # calculate the distance

        override_msg.channels[index[req.direction]] = 1500 # set speed to 1500 (stop)
        self.control_msg_pub.publish(override_msg) # publish the stop msg
        self.rate.sleep()
        location2 = self._dist_tools.get_coor() # update location
        rospy.loginfo("The vehicle travelled a distance of: %f successfully",self.calc_distance(location1,location2))
        return True # return true for success

if __name__ == '__main__': # main funciton
    rospy.init_node('long_lat_control_serviceServer')
    object__ = long_lat_control()
    rospy.spin()
