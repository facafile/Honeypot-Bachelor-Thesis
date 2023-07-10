FROM imunes/vroot-python:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./common/power-grid-simulator-master /scada/power-grid-simulator-master
ADD ./process/process-docker-script.sh /process-docker-script.sh

COPY client.py client.py

RUN /process-docker-script.sh

CMD source /scada/.venv/bin/activate && \
    cd /scada/power-grid-simulator-master/ && \
    python -m simulator.main
   

# docker build -t imunes/vroot-process -f Dockerfile.process .
