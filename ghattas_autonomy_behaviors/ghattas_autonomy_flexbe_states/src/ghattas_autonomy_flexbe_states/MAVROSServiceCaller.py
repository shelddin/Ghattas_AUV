#!/usr/bin/env python
import rospy
import sys
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller

# Import the service type from MAVROS
from mavros_msgs.srv import CommandBool, CommandBoolRequest
from mavros_msgs.srv import SetMode, SetModeRequest
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

class MAVROSServiceCaller(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- target_time 	float 	Time which needs to have passed since the behavior started.

	<= continue 			Given time has passed.
	<= failed 				Example for a failure outcome.

	'''

	def __init__(self, target, service_name, srv_type):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(MAVROSServiceCaller, self).__init__(outcomes = ['Done', 'Failed'])
		#To catch the sent srv_type in the state parameter
		types = {"CommandBool" : CommandBool, "SetMode" : SetMode}
		self._topic = service_name
		self._target = target
		self._srv_type = types[srv_type]
		self.service_client = ProxyServiceCaller({self._topic: self._srv_type}) # pass required clients as dict (topic: type)
		#self._proxy = rospy.ServiceProxy(self._topic,dist)
		# Store state parameter for later use.
		Logger.loginfo("initiated %s service caller" %self._topic)
		# The constructor is called when building the state machine, not when actually starting the behavior.
		# Thus, we cannot save the starting time now and will do so later
		#if srv_type == "SetMode":
		#	temp = self._target
		#	self._targe = SetModeRequest()
		#	self._target.custom_mode = temp


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		if self._srv_type == SetMode:
			Logger.loginfo("In the if statement")
			Logger.loginfo("Executing The service %s and sending "%self._topic)
			self.service_client.call(self._topic,SetModeRequest(0,self._target))
		else:
			Logger.loginfo("Executing The service %s and sending "%self._topic)
			self.service_client.call(self._topic,self._target)


		return 'Done' # One of the outcomes declared above.

	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		# The following code is just for illustrating how the behavior logger works.
		# Text logged by the behavior logger is sent to the operator and displayed in the GUI.
		pass



	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		pass# In this example, we use this event to set the correct start time.


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
