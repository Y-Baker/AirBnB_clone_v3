#!/usr/bin/env bash
#script to initialize the dependencies
sudo apt-get update -y
sudo apt-get install python3-dev -y
sudo apt-get install libmysqlclient-dev
sudo apt-get install pkg-config libmysqlclient-dev
sudo apt-get install libmysqlclient-dev
sudo apt-get install zlib1g-dev
pip3 install mysqlclient

pip3 install SQLAlchemy

pip3 uninstall Fabric
sudo apt-get install libffi-dev
sudo apt-get install libssl-dev
sudo apt-get install build-essential
sudo apt-get install python3.4-dev
sudo apt-get install libpython3-dev
pip3 install pyparsing
pip3 install appdirs
pip3 install setuptools==40.1.0
pip3 install cryptography==2.8
pip3 install bcrypt==3.1.7
pip3 install PyNaCl==1.3.0
pip3 install Fabric3==1.14.post1
pip3 install Flask
