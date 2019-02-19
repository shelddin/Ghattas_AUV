#!/bin/bash

cd $HOME

# add ROS ppa
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

sudo apt update
sudo apt upgrade

# Install ROS
sudo apt-get install ros-kinetic-desktop-full
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential

# install additional ROS packages 
sudo apt-get install ros-kientic-rosserial-arduino
sudo apt-get install ros-kinetic-rosserial

# Install opencv required deps
sudo apt install htop
sudo apt install python-pip
sudo pip2 install --upgrade pip
sudo pip2 install imutils
python -m pip install --upgrade --user mss
sudo apt install cmake python-dev python-numpy
sudo apt install gcc g++
sudo apt install python-gtk2-dev
sudo apt install libffms2-4
sudo apt install gstreamer1.0-plugins-base
sudo apt install git

# clone and build latest stable opencv version
cd $HOME
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

# creat, install needed deps and build workspace
cd $HOME
mkdir ~/ghattas/src/
cd ~/ghattas/
git clone https://github.com/ShehabAldeen/Ghattas_AUV/ ~/ghattas/src/
cd ~/ghattas/src/
git clone https://github.com/team-vigir/flexbe_behavior_engine.git
git clone https://github.com/FlexBE/flexbe_app.git
sudo apt-get install ros-kinetic-mavros ros-kinetic-mavros-extras
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
chmod +x ./install_geographiclib_datasets.sh
sudo ./install_geographiclib_datasets.sh
rm ./install_geographiclib_datasets.sh

#source /opt/ros/kinetic/setup.bash
cd ~/ghattas/
catkin_make
source devel/setup.bash

