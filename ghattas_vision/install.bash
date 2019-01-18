#!/bin/bash

direct=$(pwd)
sudo apt update
sudo apt upgrade

sudo apt install htop
sudo apt install python-pip
sudo pip2 install --upgrade pip
sudo pip2 install imutils
sudo apt install cmake python-dev python-numpy
sudo apt install gcc g++
sudo apt install python-gtk2-dev
sudo apt install libffms2-4
sudo apt install gstreamer1.0-plugins-base
sudo apt install git
mkdir opencv-source
cd opencv-source
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib
mkdir build
cd build
cmake -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules ../opencv
# make
# sudo make install
cd ${direct}
read -p 'press enter to clear temp folders' $x
yes | rm -r opencv-source

