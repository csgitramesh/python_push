#!/bin/bash
sudo yum update -y            # Update system packages
sudo yum install python3 -y   # Install Python 3 (if not already installed)
sudo yum install python3-pip -y  # Install pip (if not already installed)

pip3 install numpy            # Install numpy
pip3 install pandas           # Install pandas
pip3 install matplotlib       # Install matplotlib
pip3 install scikit-learn     # Install scikit-learn

