#!/usr/bin/env python
import rospy
import rostopic
import inspect
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyPublisher

class launch_torpedo(EventState):
	'''
	state to launch the torpedo.
	this will launch one torpedo no inputs needed.


	<= launched 			the torpedo launched successfully.


	'''

	def __init__(self):
		super(Drop_Marker, self).__init__(outcomes = ['launched'])

		self._topic = "arduino/launch_torpedo"
		(msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
		if msg_topic == self._topic:
			msg_type = self._get_msg_from_path(msg_path)
			self._publisher = ProxyPublisher({self._topic: msg_type})


	def execute(self, userdata):
        self._publisher.publish(self._topic, Empty())

	def on_enter(self, userdata):
        pass

	def on_exit(self, userdata):
		pass


	def on_start(self):
        pass


	def on_stop(self):
		pass
