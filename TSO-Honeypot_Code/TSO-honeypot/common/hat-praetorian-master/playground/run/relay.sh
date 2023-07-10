#!/bin/sh

RUN_PATH=$(cd $(dirname -- "$0") && pwd)
ROOT_PATH=$RUN_PATH/../..
GEN_PATH=$RUN_PATH/gen/relay/

export PYTHONPATH=$ROOT_PATH/src_py

mkdir -p $GEN_PATH

python -m hat.praetorian.relay.system \
    --conf-path $ROOT_PATH/src_doit/dist/relay.yaml \
    --gen-path $GEN_PATH \
    "$@"
