# Ghattas_AUV
software system developed for autonomous underwater vehicle (AUV) for RoboSub 2019 competition based on Robotics Operating System (ROS) and ArduSub firmware

## Description

### ghattas_control:
contains all the necessary movements for the vehicle using ROS services
#### Subscribe

#### Publish

#### Service

### ghattas_control (arduino):
#### Subscribe
**/arduino/launch_torpedo** of message type [std_msgs/Empty](https://docs.ros.org/lunar/api/std_msgs/html/msg/Empty.html)

**/arduino/open_dropper** of message type [std_msgs/Empty](https://docs.ros.org/lunar/api/std_msgs/html/msg/Empty.html)

**/arduino/open_gripper** of message type [std_msgs/Empty](https://docs.ros.org/lunar/api/std_msgs/html/msg/Empty.html)

**/arduino/close_gripper** of message type [std_msgs/Empty](https://docs.ros.org/lunar/api/std_msgs/html/msg/Empty.html)

### mavros_launcher:
here all necessary configuration files using YAML file type to configure the whole system and launch it in one launch file
#### Subscribe

#### Publish

#### Service



### ghattas_vision:
Provides image processing functionality, and video stream for other Packages.
#### Subscribe
*TBA*
#### Publish
**/zed_camera/left_img_rect** of message type [sensor_msgs/Image](https://docs.ros.org/kinetic/api/sensor_msgs/html/msg/Image.html) ***!! use this for monoculer operations***

**/zed_camera/right_img_rect** of message type [sensor_msgs/Image](https://docs.ros.org/kinetic/api/sensor_msgs/html/msg/Image.html)

**/vision/detection** of message type [ghattas_vision/vision_task_detection]

**/vision/gate** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)

**/vision/bouy** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)

**/vision/path** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)

**/vision/torpedo** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)

**/vision/markdropper** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)

**/vision/gripper** of message type [geometry_msgs/Transform Message](https://docs.ros.org/api/geometry_msgs/html/msg/Transform.html)



### ghattas_autonomoy_behaviors:
all the states and behaviours for the FlexBe state-machine to be here
#### Subscribe

#### Publish

#### Service



### ghattas_localization:
#### Subscribe

#### Publish

#### Service



## Used 3rd Party Packages:
### darknet_ros [github](https://github.com/leggedrobotics/darknet_ros)
Used to integrate Yolo object detection.
#### Subscribe
**/camera/rgb/image_raw** remaped to **/zed_camera/left_img_rect** of message type [sensor_msgs/Image](https://docs.ros.org/kinetic/api/sensor_msgs/html/msg/Image.html)

#### Publish
**/object_detector** ([std_msgs::Int8])

Publishes the number of detected objects.

**/bounding_boxes** ([darknet_ros_msgs::BoundingBoxes])

Publishes an array of bounding boxes that gives information of the position and size of the bounding box in pixel coordinates.

**detection_image** ([sensor_msgs::Image])

Publishes an image of the detection image including the bounding boxes.
