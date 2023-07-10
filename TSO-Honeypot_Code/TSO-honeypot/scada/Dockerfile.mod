FROM imunes/vroot-scada:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./hat-mod /scada/hat-quickstart
ADD ./common/resolv.conf /etc/resolv.conf

RUN source /scada/.venv/bin/activate && \
    cd /scada/hat-quickstart/ && \
    doit js_view

CMD source /scada/.venv/bin/activate && \
    cd /scada/hat-quickstart/playground/run && \
    ./system.sh

# docker build -t imunes/vroot-scada-mod -f Dockerfile.mod .
