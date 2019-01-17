#!/usr/bin/env python
import sys
import rospy
import time
from std_srvs.srv import Empty, EmptyResponse
from std_msgs.msg import Float64
from mavros_msgs.msg import OverrideRCIn
from smach_mavros_ardusub_test.srv import hdg, hdgRequest


class move_square (object):

    def __init__(self):
        self.init_hdg()
        self.hdg_subscriber = rospy.Subscriber('/mavros/global_position/compass_hdg'
                                               , Float64, self.hdg_callback,queue_size=1)
        self.rc_publisher = rospy.Publisher("/mavros/rc/override", OverrideRCIn,
                                            queue_size=10)
        self.serv = rospy.Service('/autonomous/move_sub_square', Empty, self.service_callback)
        self.rc_msg = OverrideRCIn()
        self.hdg_req = hdgRequest()
        self.rate = rospy.Rate(10)
        rospy.loginfo("The move square service is READY")

    def init_hdg(self):
        self._hdg = None
        while self._hdg is None:
            try:
                self._hdg = rospy.wait_for_message("/mavros/global_position/compass_hdg",
                                                   Float64, timeout=1)
            except:
                rospy.loginfo("/compass_hdg topic is not ready yet, retrying")

        rospy.loginfo("/compass_hdg topic READY")

    def hdg_callback(self,msg):
        self.current_heading = msg

    def get_current_hdg (self):
        return self.current_heading.data

    def service_callback(self, req):
        x = 0
        while(x < 4):
            current_heading = self.get_current_hdg()
            rospy.loginfo("moving forward")
            self.move_forward()
            nxt_heading = self.calculate_nxt_heading(current_heading)
            rospy.loginfo("next heading to be reached is : %f",nxt_heading)
            self.call_heading_to(nxt_heading)

            x = x + 1
        self.stop()

    def move_forward(self):
        self.rc_msg.channels[4] = 1900
        self.rc_publisher.publish(self.rc_msg)
        rospy.sleep(10)
        self.rc_msg.channels[4] = 1500
        self.rc_publisher.publish(self.rc_msg)
        self.rate.sleep()

    def stop(self):
        self.rc_msg.channels = [1500 for r in range(len(self.rc_msg.channels))]
        self.rc_publisher.publish(self.rc_msg)
        self.rate.sleep()
        rospy.loginfo("Stopped ...")

    def call_heading_to(self,heading):
        self.hdg_req.desired_hdg = heading
        rospy.wait_for_service("/autonomous/heading_to")
        try:
            client = rospy.ServiceProxy('/autonomous/heading_to', hdg)
            resp = client(self.hdg_req)
            if resp:
                rospy.loginfo("90 degree turned successfully")
                return resp
            else:
                rospy.logerr("something wrong happened while calling heading to service")
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    def calculate_nxt_heading(self,heading = 0):
        nxt = heading - 90
        if nxt > 0:
            return nxt
        elif nxt < 0:
            nxt = 360 - abs(nxt)
            return nxt

if __name__ == "__main__":
    rospy.init_node("move_squareService")
    square_object = move_square()
    rospy.spin()
