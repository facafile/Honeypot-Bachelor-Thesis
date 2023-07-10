#!/bin/sh

INSTALL_PATH=/opt/hat-eds
PYTHON=$INSTALL_PATH/bin/python

exec $PYTHON ./command_attack.py \
    "$@"
