FROM imunes/vroot-python:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./scada-praetorean/scada-praetorean-docker-script.sh /scada-praetorean-docker-script.sh
ADD ./common/hat-praetorian-master /scada/hat-praetorean-master
ADD ./common/resolv.conf /etc/resolv.conf

RUN apt install -y git
RUN /scada-praetorean-docker-script.sh

CMD source /scada/.venv/bin/activate && \
    cd /scada/hat-praetorean-master/ && \
#    ./playground/run/commander.sh & && \
    ./playground/run/relay.sh
#    ./playground/run/manager.sh

# docker build -t imunes/vroot-scada-praetorean -f Dockerfile .
