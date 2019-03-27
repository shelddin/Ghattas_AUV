#!/usr/bin/env python
import rospy
import sys
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller

# Import the service type
from ghattas_control.srv import dist, distResponse
from ghattas_control.srv import depth, depthResponse
from ghattas_control.srv import hdg, hdgResponse
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

class precise_movement(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- target_heading 	float 	Time which needs to have passed since the behavior started.

	<= Done 			Given time has passed.
	<= Failed 				Example for a failure outcome.

	'''

	def __init__(self, mode, target_distance):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(MovementServiceCaller, self).__init__(outcomes = ['Done', 'Failed'])
		#To catch the sent srv_type in the state parameter
		self._topic = "/autonomous/precise_movement"
		self._srv_type = dist
		self._mode = mode
        self._target = target_distance
		self.service_client = ProxyServiceCaller({self._topic: self._srv_type}) # pass required clients as dict (topic: type)
		Logger.loginfo("initiated %s service caller" %self._topic)

	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.

		Logger.loginfo("Executing The service %s"%self._topic)
		self.service_client.call(self._topic,self._mode,self._target)



		return 'Done' # One of the outcomes declared above.

		# If no outcome is returned, the state will stay active.
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
