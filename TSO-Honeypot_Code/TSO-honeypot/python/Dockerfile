FROM imunes/vroot:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./python/install-python.sh /install-python.sh
ADD ./common/resolv.conf /etc/resolv.conf

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN /install-python.sh

CMD while true; do sleep infinity; done

# docker build -t imunes/vroot-python -f Dockerfile.python .
