#!/bin/bash

source /scada/.venv/bin/activate

# Install process dependencies
pip3 install --upgrade pip
cd /scada/power-grid-simulator-master/
pip3 install -r requirements.txt

echo "Process simulator initialized!"

