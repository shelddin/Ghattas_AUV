#!/bin/bash

# wait system to fully load
sleep 30

# launch code starts here
cd ~/ghattas/
source devel/setup.bash

#~/ghattas/src/bash_scripts/zed_launch.bash

nohup xterm -hold -e roscore &
nohup xterm -hold -e rosrun rosserial_python serial_node.py _port:=/dev/ttyACM1 &
nohup xterm -hold -e roslaunch ghattas_launcher ghattas.launch &
