#!/bin/bash

source /scada/.venv/bin/activate

# Install SCADA services
pip3 install --upgrade pip
cd /scada/hat-praetorean-master/
pip3 install -r requirements.pip.dev.txt
pip3 install -r requirements.pip.runtime.txt
doit js_view

echo "SCADA initialized!"
