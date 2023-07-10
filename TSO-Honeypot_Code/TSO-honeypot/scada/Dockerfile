FROM imunes/vroot-python:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./scada/scada-docker-script.sh /scada-docker-script.sh
ADD ./common/hat-quickstart /scada/hat-quickstart
ADD ./common/resolv.conf /etc/resolv.conf

RUN /scada-docker-script.sh

CMD source /scada/.venv/bin/activate && \
    cd /scada/hat-quickstart/playground/run && \
    ./system.sh

# docker build -t imunes/vroot-scada -f Dockerfile.scada .
