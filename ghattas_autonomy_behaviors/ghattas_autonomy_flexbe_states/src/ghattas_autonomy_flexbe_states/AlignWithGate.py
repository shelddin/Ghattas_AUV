#!/usr/bin/env python
import rospy
import sys
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller,ProxySubscriberCached
from ghattas_vision.msg import vision_target
# Import the service type from MAVROS
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest

class AlignWithGate(EventState):

	#To be developed according to the optimization notes
	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(AlignWithGate, self).__init__(outcomes = ['Aligned', 'CantSee'])
		#To catch the sent srv_type in the state parameter
		self._v_topic = "/vision/gate"
		self.sway_left_client = ProxyServiceCaller({'/autonomous/sway_left': Empty}) # pass required clients as dict (topic: type)
		self.sway_right_client = ProxyServiceCaller({'/autonomous/sway_right': Empty}) # pass required clients as dict (topic: type)
		self.heave_down_client = ProxyServiceCaller({'/autonomous/heave_down': Empty}) # pass required clients as dict (topic: type)
		self.heave_up_client = ProxyServiceCaller({'/autonomous/heave_up': Empty}) # pass required clients as dict (topic: type)
		self.stop_client = ProxyServiceCaller({'/autonomous/stop_vehicle': Empty}) # pass required clients as dict (topic: type)
		self.vision_sub = ProxySubscriberCached({self._v_topic: vision_target})
		self.inrange_flag = True
		Logger.loginfo("initiated allign gate state")

	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		Logger.loginfo("executing Align with gate")
		self.update_subscriber()
		if self.vision_sub.has_msg(self._v_topic):
			Logger.loginfo("There is a msg coming")
			if  self.inrange_flag:
				Logger.loginfo("start aligning with gate")
				self.allign_in_z()
				self.allign_in_x()
				Logger.loginfo("Aligned with gate")
				return "Aligned"
			else:
				Logger.loginfo("cant find the gate")
				return "CantSee"


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
	def sway_left(self):
	    self.sway_left_client.call('/autonomous/sway_left',EmptyRequest())
	def sway_right(self):
	    self.sway_right_client.call('/autonomous/sway_right',EmptyRequest())
	def heave_down(self):
	    self.heave_down_client.call('/autonomous/heave_down',EmptyRequest())
	def heave_up(self):
	    self.heave_up_client.call('/autonomous/heave_up',EmptyRequest())
	def stop(self):
	    self.stop_client.call('/autonomous/stop_vehicle',EmptyRequest())

	def update_subscriber (self):
		if self.vision_sub.has_msg(self._v_topic):
			msg = self.vision_sub.get_last_msg(self._v_topic)
			self.ValZ = msg.z
			self.ValX = msg.x
			self.inrange_flag = msg.found

	def allign_in_z(self):
		self.update_subscriber()
		Logger.loginfo("started aligning in Z ...")
		while (390 > self.ValZ or self.ValZ > 590):
			while (self.ValZ > 590):
				self.heave_up()
				self.update_subscriber()
			self.stop()
			while (self.ValZ < 390):
				self.heave_down()
				self.update_subscriber()
			self.stop()
			self.update_subscriber()
		rospy.loginfo("Alligned in Z = %f...",self.ValZ)

	def allign_in_x(self):
		self.update_subscriber()
		Logger.loginfo("started aligning in X ...")
		while (910 > self.ValX or self.ValX > 1010):
			rospy.loginfo("X = %f...",self.ValX)
			while (self.ValX > 1010):
				self.sway_right()
				rospy.loginfo("X = %f...",self.ValX)
				self.update_subscriber()
			self.stop()
			while (self.ValX < 910):
				self.sway_left()
				self.update_subscriber()
			self.stop()
			self.update_subscriber()
		Logger.loginfo("Aligned in X")

#class align_tools(object):
