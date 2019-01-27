#!/usr/bin/env python
import rospy
import pickle
from std_msgs.msg import Float64
from geometry_msgs.msg import Point, PoseStamped


current = {'heading':0,
'x':0,
'y':0,
'z':1}


def pickle_it():
	global current
	with open('current.pkl', 'wb') as pickle_file:
		pickle.dump(current,pickle_file)
		print('pickled')

def heading(msg):
	global current
	print('got hdg')
	current['heading'] = msg.data
	pickle_it()

def pose(msg):
	global current
	print('got pose')
	current['x'] = msg.pose.position.x
	current['y'] = msg.pose.position.y
	current['z'] = msg.pose.position.z+4
	pickle_it()

rospy.init_node('blender')
rospy.Subscriber("/mavros/global_position/compass_hdg", Float64, heading)
rospy.Subscriber("/mavros/local_position/pose/", PoseStamped, pose)


pickle_it()
rospy.spin()
