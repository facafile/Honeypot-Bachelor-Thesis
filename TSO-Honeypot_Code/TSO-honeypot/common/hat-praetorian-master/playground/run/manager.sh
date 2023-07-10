#!/bin/sh

RUN_PATH=$(cd $(dirname -- "$0") && pwd)
ROOT_PATH=$RUN_PATH/../..
GEN_PATH=$RUN_PATH/gen

export PYTHONPATH=$ROOT_PATH/src_py

mkdir -p $GEN_PATH

python -m hat.manager \
    --conf $GEN_PATH/manager.yaml \
    "$@"
