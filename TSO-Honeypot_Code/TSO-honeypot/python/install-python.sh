#!/bin/bash

# Install Python 3.9 and other required packages
apt update
apt install -y gnupg2 libsqlite3-dev libffi-dev libbz2-dev liblzma-dev
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
apt update
apt install -y yarn nodejs
yarn --version

mkdir /scada
cd /scada
wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz
tar xzf Python-3.9.13.tgz
cd Python-3.9.13
./configure --enable-loadable-sqlite-extensions --enable-optimizations
make && make altinstall
./python -m venv /scada/.venv
source /scada/.venv/bin/activate

echo "Python installed!"

