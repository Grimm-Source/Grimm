#!/bin/bash

sudo apt update
sudo apt install --assume-yes curl
sudo curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
sudo python3 /tmp/get-pip.py --user
sudo rm /tmp/get-pip.py
sudo apt --assume-yes install python3-pip
sudo apt --assume-yes install python3-dev
sudo apt --assume-yes install build-essential
sudo apt --assume-yes install libssl-dev
sudo apt --assume-yes install libffi-dev
sudo apt --assume-yes install python3-setuptools
sudo apt --assume-yes install nginx
sudo add-apt-repository ppa:certbot/certbot
sudo apt --assume-yes install python-certbot-nginx
sudo apt --assume-yes install openssl

# mysql server
sudo apt --assume-yes install mysql-server
sudo apt --assume-yes autoremove
sudo apt --assume-yes autoclean
sudo mysql_secure_installation

