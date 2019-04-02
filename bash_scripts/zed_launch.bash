#!/bin/bash

"/usr/local/zed/tools/ZED Explorer" &
PID=`jobs -p`

sleep 15

kill $PID

sleep 15

python ~/Desktop/zed_test.py
