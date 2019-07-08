#!/bin/bash

# prepare system before install
cd $HOME
sudo apt update
sudo apt upgrade
sudo apt install git
sudo apt install python-pip

# ROV networking packages
sudo apt install openssh-server
sudo apt install arp-scan

# ROS
# add ROS ppa
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

sudo apt update
sudo apt upgrade

# Install ROS
sudo apt-get install ros-kinetic-desktop-full
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
echo "source ~/ghattas/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential

# install additional ROS-packages
sudo apt-get install ros-kientic-rosserial-arduino
sudo apt-get install ros-kinetic-rosserial
sudo apt install ros-kinetic-ddynamic-reconfigure
sudo apt install ros-kinetic-ddynamic-reconfigure-python

# creat, install needed deps and build workspace
# clone ghattas repo to work-space
cd $HOME
mkdir ~/ghattas/src/
cd ~/ghattas/
git clone https://github.com/ShehabAldeen/Ghattas_AUV/ ~/ghattas/src/
cd ~/ghattas/src/
# clone flexbe behavior engine to work-space
git clone https://github.com/team-vigir/flexbe_behavior_engine.git
git clone https://github.com/FlexBE/flexbe_app.git
# install MavLink, MavROS & MavProxy
sudo apt-get install ros-kinetic-mavros ros-kinetic-mavros-extras
sudo pip install --upgrade pymavlink MAVProxy
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
chmod +x ./install_geographiclib_datasets.sh
sudo ./install_geographiclib_datasets.sh
rm ./install_geographiclib_datasets.sh
# clone darknet_ros
git clone --recursive https://github.com/leggedrobotics/darknet_ros

# Install camera drivers
# intel Realsense T256
echo 'deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main' | sudo tee /etc/apt/sources.list.d/realsense-public.list
sudo apt-key adv --keyserver keys.gnupg.net --recv-key 6F3EFCDE
sudo apt update
sudo apt install librealsense2-dkms
sudo apt install librealsense2-utils
sudo apt install librealsense2-dev
sudo apt install librealsense2-dbg
cd ~ghattas/src
git clone https://github.com/intel-ros/realsense

# zed-mini
mkdir ~/temp/
cd ~/temp/
wget "https://www.stereolabs.com/developers/downloads/ZED_SDK_Ubuntu16_v2.8.0.run"
chmod +x ZED_SDK_*.run
./ZED_SDK_*.run

# build work=space
source /opt/ros/kinetic/setup.bash
cd ~/ghattas/
catkin_make -DCMAKE_BUILD_TYPE=Release
source devel/setup.bash

# OPENCV
# Install opencv required deps
sudo pip2 install --upgrade pip
sudo pip2 install imutils
python -m pip install --upgrade --user mss
sudo apt install cmake python-dev python-numpy
sudo apt install gcc g++
sudo apt install python-gtk2-dev
sudo apt install libffms2-4
sudo apt install gstreamer1.0-plugins-base

# clone and build latest stable opencv version
cd $HOME/temp/
mkdir opencv-source
cd opencv-source
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib
mkdir build
cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -D CMAKE_INSTALL_PREFIX=/opt/ros/kinetic/ ../opencv
make
sudo make install
#cd $HOME
#read -p 'press enter to clear temp folders' $x
#yes | rm -r opencv-source

# setup automatic system startup (uncomment when installing on vehicle)
#echo "nohup ~/ghattas/src/bash_scripts/launch.bash &" >> ~/.profile #.profile might change to ~/.bash_profile/~/.bash_login/~/.profile (the first one available following the order).

# install optional user convenienc packages
sudo add-apt-repository ppa:webupd8team/terminix
sudo apt update
sudo apt install tilix
sudo apt install htop
