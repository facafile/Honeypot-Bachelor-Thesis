FROM imunes/vroot-python:latest

COPY server.py /app/server.py
COPY server2.py /app/server2.py

EXPOSE 8080
EXPOSE 8081

CMD python3 /app/server.py && \
    python3 /app/server2.py
