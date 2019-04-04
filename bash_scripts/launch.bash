#!/bin/bash

# wait system to fully load
sleep 30

# launch code starts here
cd ~/ghattas/
source devel/setup.bash

#~/ghattas/src/bash_scripts/zed_launch.bash

nohup xterm -e roslaunch ghattas_launcher ghattas.launch
