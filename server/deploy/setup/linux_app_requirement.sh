#!/bin/bash

sudo apt update
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
sudo mysql_secure_installation

