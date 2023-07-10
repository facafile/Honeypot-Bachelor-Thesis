FROM imunes/vroot:latest
MAINTAINER Ivan Kovačević <ivan.kovacevic.fer@gmail.com>

ADD ./common/resolv.conf /etc/resolv.conf

RUN apt update && \
    apt install -y sqlite3 && \
    sqlite3 historian.db

CMD
