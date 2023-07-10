FROM imunes/vroot-python:latest
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y snort && \
    rm -rf /var/lib/apt/lists/*
    
COPY snort.conf /etc/snort/snort.conf

RUN apt-get update && apt-get install -y build-essential wget libpcap-dev libtool autoconf
WORKDIR /opt
RUN wget https://github.com/firnsy/barnyard2/archive/master.tar.gz
RUN tar -xvf master.tar.gz && mv barnyard2-master barnyard2
WORKDIR /opt/barnyard2
RUN ./autogen.sh && ./configure && make && make install
RUN rm -rf /opt/master.tar.gz



#CMD ["snort", "-A", "console","-i","eth0", "-c", "/etc/snort/snort.conf"]alert_syslog
