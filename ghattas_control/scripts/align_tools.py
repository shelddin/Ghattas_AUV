
#!/usr/bin/env python
import rospy
import sys
from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxyServiceCaller
from gharras_vision.msg import vision_target
# Import the service type from MAVROS
from std_srvs.srv import Empty, EmptyResponse, EmptyRequest


class align_tools(object):

	def sway_left(self):
	    self.sway_left_client.call('/autonomous/sway_left',EmptyRequest())
	def sway_right(self):
	    self.sway_right_client.call('/autonomous/sway_right',EmptyRequest())
	def surge_forward(self):
	    self.heave_down_client.call('/autonomous/heave_down',EmptyRequest())
	def surge_backward(self):
	    self.heave_up_client.call('/autonomous/heave_up',EmptyRequest())
	def stop(self):
	    self.stop_client.call('/autonomous/stop_vehicle',EmptyRequest())

	def update_subscriber (self):
	    msg = vision_sub.get_last_msg(self._v_topic)
	    self.ValZ = msg.z
	    self.ValX = msg.x
	    self.inrange_flag = msg.found

	def allign_in_z(self):
	    self.update_subscriber()
	    while (390 > self.ValZ or self.ValZ > 590):
	        while (self.ValZ > 590):
	            self.sway_left()
	            self.update_subscriber()
	        self.stop()
	        while (self.ValZ < 390):
	            self.sway_right()
	            self.update_subscriber()
	        self.stop()
	        self.update_subscriber()


	def allign_in_x(self):
	    self.update_subscriber()
	    while (910 > self.ValX or self.ValX > 1010):
	        while (self.ValX > 1010):
	            self.heave_down()
	            self.update_subscriber()
	        self.stop()
	        while (self.ValX < 910):
	            self.sway_right()
	            self.update_subscriber()
	        self.stop()
	        self.update_subscriber()
