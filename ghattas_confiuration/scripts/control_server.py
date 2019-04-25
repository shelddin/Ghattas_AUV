#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from ghattas_confiuration.cfg import control_reconfigureConfig

def callback(config, level):
#    rospy.loginfo("""Reconfigure Request: {int_param}, {double_param},\
#          {str_param}, {bool_param}, {size}""".format(**config))
    rospy.loginfo(config)
    return config

if __name__ == "__main__":
    rospy.init_node("control_reconfigure", anonymous = False)

    srv = Server(control_reconfigureConfig, callback)
    rospy.spin()
