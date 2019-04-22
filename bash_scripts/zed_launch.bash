#!/bin/bash

"/usr/local/zed/tools/ZED Explorer" &
PID=`jobs -p`

sleep 10

kill $PID
