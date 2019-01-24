#!/usr/bin/env python
import rospy
import pickle
from std_msgs.msg import Float32

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
	current['heading'] = msg.data
	pickle_it()
def x(msg):
	global current
	current['x'] = msg.data
	pickle_it()
def y(msg):
	global current
	current['y'] = msg.data
	pickle_it()
def z(msg):
	global current
	current['z'] = msg.data
	pickle_it()


rospy.init_node('blender')
rospy.Subscriber("/heading", Float32, heading)
rospy.Subscriber("/x", Float32, x)
rospy.Subscriber("/y", Float32, y)
rospy.Subscriber("/z", Float32, z)


rospy.spin()
