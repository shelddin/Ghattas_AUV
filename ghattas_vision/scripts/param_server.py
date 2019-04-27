#!/usr/bin/env python
import rospy
from dynamic_reconfigure.server import Server
from ghattas_vision.cfg import vision_dynamic_reConfig


def callback(config, level):
    #rospy.loginfo("""Reconfigure Request: """config)
    print(config)
    return config

if __name__ == "__main__":
    rospy.init_node("vision_param")

    srv = Server(vision_dynamic_reConfig, callback)
    rospy.spin()
