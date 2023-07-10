FROM imunes/vroot-python:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tshark

#COPY capture_and_send.py /home/capture_and_send.py
COPY start.sh /home/start.sh 

RUN setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/bin/dumpcap

ENTRYPOINT ["/home/start.sh"]

#CMD ["python", "/home/capture_and_send.py"]



