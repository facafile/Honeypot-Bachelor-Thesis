#!/bin/sh

RUN_PATH=$(cd $(dirname -- "$0") && pwd)
ROOT_PATH=$RUN_PATH/../..
GEN_PATH=$RUN_PATH/gen/commander/

export PYTHONPATH=$ROOT_PATH/src_py

mkdir -p $GEN_PATH

python -m hat.praetorian.commander.system \
    --conf-path $ROOT_PATH/src_doit/dist/commander.yaml \
    --gen-path $GEN_PATH \
    "$@"
