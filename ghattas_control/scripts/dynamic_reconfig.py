#!/usr/bin/env python

import rospy
from dynamic_reconfigure.server import Server
from ghattas_control.cfg import control_reconfigureConfig

def callback(config, level):
    rospy.loginfo(config)
    return config

if __name__ == "__main__":
    rospy.init_node("control_reconfigure", anonymous = False)

    srv = Server(control_reconfigureConfig, callback)
    rospy.spin()
