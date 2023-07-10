#!/bin/bash
# To be run prior to starting any IMUNES experiments

echo "Building Docker containers..."
date

docker build -t imunes/vroot-conpot -f conpot/Dockerfile .
docker build -t imunes/vroot-python -f python/Dockerfile .
docker build -t imunes/vroot-scada -f scada/Dockerfile .
docker build -t imunes/vroot-scada-mod -f scada/Dockerfile.mod .
docker build -t imunes/vroot-scada-praetorean -f scada-praetorean/Dockerfile .
docker build -t imunes/vroot-process -f process/Dockerfile .

echo "Docker containers built!"
date
