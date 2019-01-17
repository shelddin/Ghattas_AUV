#!/usr/bin/env python
import rospy
import rostopic
import inspect
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached

'''
Created on 02.01.2019

@author: Ahmad Aljabali
'''

class AlignmentWatchState(EventState):
	'''
	Implements a state that can find the error based on userdata.
	error_calculation is a function which takes reference and measured values,
	that will be stored in input_value from userdata,their keys should be provided to the state,
	and it returns the euclidean distance in output_value after leaving the state.

	-- topic        string      Topic where the mesured result is published.
	-- tolerance	number		The acceptable error for operations (absolute error).
	-- keys	        string[]	The key for the values to calculate the error.
	-- referance    object      The referance ideal value.

	#> output_value object		The calculated error.

	<= unacceptable				Indicates an error that excedes tolerance.
	<= success					Indicates no need for alignment check anymore.
	'''


	def __init__(self, topic, tolerance, keys, reference):
		'''
		Constructor
		'''
		super(AlignmentWatchState, self).__init__(outcomes=['unacceptable','success'],
													output_keys=['output_value'])


		self._tolerance = tolerance
		self._keys = keys
		self._reference = reference
		self._error_result = {}
		self._topic = topic
		(msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
		if msg_topic == self._topic:
			msg_type = self._get_msg_from_path(msg_path)
			self._subscriber = ProxySubscriberCached({self._topic: msg_type})


	def execute(self, userdata):
		'''Execute this state'''
		if self._subscriber.has_msg(self._topic):
			msg = self._subscriber.get_last_msg(self._topic)
			# in case you want to make sure the same message is not processed twice:
			self._subscriber.remove_last_msg(self._topic)
			if not msg.found:
				return 'success'

			self.calculate_error(msg)
			Logger.loghint(self._error_result)

			for key in self._keys:
				# check tolerance
				if self._tolerance < abs(self._error_result[key]):
					userdata.output_value = self._error_result
					return 'unacceptable'


	def on_enter(self, userdata):
		pass

	def calculate_error(self, measured):
		Logger.loginfo('calculating error')
		for key in self._keys:
			self._error_result[key]=self._reference[key]-getattr(measured,key)

	def _get_msg_from_path(self, msg_path):
		msg_import = msg_path.split('/')
		msg_module = '%s.msg' % (msg_import[0])
		package = __import__(msg_module, fromlist=[msg_module])
		clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
		return clsmembers[0][1]
