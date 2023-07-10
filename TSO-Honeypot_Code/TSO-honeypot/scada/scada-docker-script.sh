#!/bin/bash

source /scada/.venv/bin/activate

# Install SCADA services
pip3 install --upgrade pip
cd /scada/hat-quickstart/
pip3 install -r requirements.pip.txt
doit js_view

echo "SCADA initialized!"
