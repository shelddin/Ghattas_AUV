#!/usr/bin/env python
import rospy
import rostopic
import inspect
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached
from rospy.exceptions import ROSInterruptException

'''
Created on 11.06.2013

@author: Philipp Schillinger
'''

class PathSelectState(EventState):
	'''
	Choose an execution path by providing its name as a string from userdata.
	This state can be used if the control flow of the behavior branches out to multiple paths.

	-- outcomes 	string[]	A list containing all possible outcomes (paths) of this state,
								'default' is reserved in case no match was found.
	-- topic		string		Topic giving mission detection status

	># input_value	string[]	List of finished mission.

	'''


	def __init__(self, topic, outcomes=['default']):
		'''
		Constructor
		'''
		super(PathSelectState, self).__init__(outcomes=outcomes,
											input_keys=['input_value'])

		self._my_outcomes = outcomes
		self._path= None
		self._PathSelected = False
		self._topic = topic
		(msg_path, msg_topic, fn) = rostopic.get_topic_type(self._topic)
		if msg_topic == self._topic:
			msg_type = self._get_msg_from_path(msg_path)
			self._subscriber = ProxySubscriberCached({self._topic: msg_type})

	def execute(self, userdata):
		'''
		Execute this state
		'''
		if self._subscriber.has_msg(self._topic):
			msg = self._subscriber.get_last_msg(self._topic)
			for outcome in self._my_outcomes:
				if getattr(msg,outcome) and outcome not in self._finished:
					self._PathSelected= True
					self._path=outcome
					return outcome

		if self._PathSelected == False:
			return 'default'


	def on_enter(self, userdata):
		self._finished=userdata.input_value


	def on_exit(self, userdata):

		if self._PathSelected == True:
			Logger.loghint('the %s path was selected' %self._path)
		else:
			Logger.logwarn('no path found fall back to default path')

	def _get_msg_from_path(self, msg_path):
		msg_import = msg_path.split('/')
		msg_module = '%s.msg' % (msg_import[0])
		package = __import__(msg_module, fromlist=[msg_module])
		clsmembers = inspect.getmembers(package, lambda member: inspect.isclass(member) and member.__module__.endswith(msg_import[1]))
		return clsmembers[0][1]
