#!/usr/bin/env python


# This is a basic state machine to drive the SUB in simple autonomous mission
# using ArduSub and MAVROS for connection all done on the SITL simulator
import roslib
import rospy
import smach
import smach_ros
from smach_ros import ServiceState, SimpleActionState
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from time import sleep
from mavros_msgs.msg import OverrideRCIn
from std_srvs.srv import Empty, EmptyRequest

class initiate_RC(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['initiated'])

    def execute(self,userdata):
        msg = OverrideRCIn()
        pub = rospy.Publisher('/mavros/rc/override',OverrideRCIn,queue_size=1000)
        msg.channels = [1500 for r in range(len(msg.channels))]
        pub.publish(msg)
        rospy.loginfo("The Channels are initiated successfully")
        return 'initiated'

        #Publisher to write to the /mavros/rc/override topic


class Dive_in(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=['succeeded'])

    def execute(self,userdata):
        rospy.loginfo("Diving in the water")
        rospy.sleep(3)
        return 'succeeded'

class move_rect(smach.State):
    def __init__ (self):
        smach.State.__init__(self,outcomes=['success'])

    def execute(self,userdata):

        rospy.loginfo("moving in a rectangle")

class move_square(smach.State):
    def __init__ (self):
        smach.State.__init__(self,outcomes=['success'])

    def execute(self,userdata):

        rospy.loginfo("moving in a square")

class set_hdg(smach.State):
    def __init__ (self):
        smach.State.__init__(self,outcomes=['success'])

    def execute(self,userdata):

        rospy.loginfo("setting the heading to : ")

class go_surface(smach.State):
    def __init__ (self):
        smach.State.__init__(self,outcomes=['success'])

    def execute(self,userdata):
        rospy.loginfo("moving up to the surface ...")
        time.sleep(3)
        return 'success'

def main():
    rospy.init_node('smach_ardusub_demo')
    sm_top = smach.StateMachine(outcomes=['succeeded','preempted','aborted'])

    with sm_top:
        #Service State to call Arm the SUB

        smach.StateMachine.add('Initiate RC channels',initiate_RC(),
                               transitions={'initiated':'Arm the Sub'})

        smach.StateMachine.add('Arm the Sub',ServiceState('/mavros/cmd/arming',
                                CommandBool,request = CommandBoolRequest(True)),
                               transitions={'succeeded':'save heading',
                                            'preempted': 'preempted',
                                            'aborted' : 'aborted'})

        # Service state to save the initial heading
        smach.StateMachine.add('save heading',ServiceState('/autonomous/save_heading'
                               ,Empty,request = EmptyRequest())
                               ,transitions={'succeeded':'change mode to Depth Hold'})


        #Service State to change the SUB mode to the manual depth hold mode
        smach.StateMachine.add('change mode to Depth Hold',ServiceState('/mavros/set_mode'
                               ,SetMode,request = SetModeRequest(0,'alt_hold'))
                               ,transitions={'succeeded':'Dive in the Water'})

        #Action State to call the DiveIn_ActionClient
        # wont use it for the first prototype
        smach.StateMachine.add('Dive in the Water',Dive_in(),
                               transitions={'succeeded':'mode to manual'})

        #Service State to change the SUB mode to the manual depth hold mode
        smach.StateMachine.add('mode to manual',ServiceState('/mavros/set_mode'
                               ,SetMode,request = SetModeRequest(0,'manual'))
                               ,transitions={'succeeded':'make square'})


        #Action State to call the move_square_ActionClient
        smach.StateMachine.add('make square',ServiceState('/autonomous/move_sub_square',
                                                          Empty,request = EmptyRequest()),
                               transitions={'succeeded':'set heading'})

        smach.StateMachine.add('set heading',ServiceState('/autonomous/heading_to_saved',
                                                          Empty, request = EmptyRequest()),
                               transitions={'succeeded':'change mode to STABILIZE'})


        #Service State to change the SUB mode to the Stabilize mode
        smach.StateMachine.add('change mode to STABILIZE',ServiceState('/mavros/set_mode'
                               ,SetMode,request = SetModeRequest(0,'stabilize'))
                               ,transitions={'succeeded':'go to surface'})


        #Action State to call the GoToSurface_ActionClient
        smach.StateMachine.add('go to surface',go_surface(),transitions={'success':'succeeded'})

    sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
    sis.start()

    outcome = sm_top.execute()

    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
