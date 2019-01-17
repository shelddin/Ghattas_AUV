cmake_minimum_required(VERSION 2.8.3)
project(ghattas_vision)

find_package(catkin REQUIRED
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
  FILES
  vision_target.msg
  vision_task_detection.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
   CATKIN_DEPENDS rospy
   CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
