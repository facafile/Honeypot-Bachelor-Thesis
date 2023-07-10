FROM imunes/vroot:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./common/resolv.conf /etc/resolv.conf

RUN chmod -R 777 /usr/local/lib/python3.6/dist-packages/conpot

CMD conpot -f --template default

# docker build -t imunes/vroot-conpot -f Dockerfile.conpot .
