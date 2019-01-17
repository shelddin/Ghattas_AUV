#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ghattas_autonomy_flexbe_states.MovementServiceCaller import MovementServiceCaller
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Dec 30 2018
@author: ShehabEldin
'''
class MovementStatemachineTestSM(Behavior):
	'''
	This a test state mcahine to ensure the integration between the MovementServiceCaller state and the movement ROS services
	'''


	def __init__(self):
		super(MovementStatemachineTestSM, self).__init__()
		self.name = 'MovementStatemachineTest'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1209 y:343, x:278 y:461
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:126 y:186
			OperatableStateMachine.add('heave_down_to',
										MovementServiceCaller(target=-5, service_name="/autonomous/heave_down_to", srv_type="depth"),
										transitions={'Done': 'sway_left_for', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:438 y:118
			OperatableStateMachine.add('surge_forward_for',
										MovementServiceCaller(target=10, service_name="/autonomous/surge_forward_for", srv_type="dist"),
										transitions={'Done': 'save_heading', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:735 y:112
			OperatableStateMachine.add('save_heading',
										MovementServiceCaller(target=0, service_name="/autonomous/save_heading", srv_type="Empty"),
										transitions={'Done': 'heading_to', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:930 y:163
			OperatableStateMachine.add('heading_to',
										MovementServiceCaller(target=200, service_name="/autonomous/heading_to", srv_type="hdg"),
										transitions={'Done': 'sway_right_for', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:932 y:33
			OperatableStateMachine.add('sway_right_for',
										MovementServiceCaller(target=5, service_name="/autonomous/sway_right_for", srv_type="dist"),
										transitions={'Done': 'heave_down_to', 'Failed': 'save_heading'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:1079 y:236
			OperatableStateMachine.add('heading_to_saved',
										MovementServiceCaller(target=0, service_name="/autonomous/heading_to_saved", srv_type="Empty"),
										transitions={'Done': 'finished', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})

			# x:365 y:31
			OperatableStateMachine.add('sway_left_for',
										MovementServiceCaller(target=5, service_name="/autonomous/sway_left_for", srv_type="dist"),
										transitions={'Done': 'surge_forward_for', 'Failed': 'failed'},
										autonomy={'Done': Autonomy.Off, 'Failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
