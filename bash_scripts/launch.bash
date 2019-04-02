#!/bin/bash

# wait system to fully load
sleep 30

# launch code starts here
# example
cheese &
PID=`jobs -p`

sleep 15

kill $PID
