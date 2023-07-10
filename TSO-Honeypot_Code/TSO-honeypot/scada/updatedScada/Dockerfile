FROM imunes/vroot-scada-mod:latest

COPY client.py client.py

RUN pip install watchdog

CMD source /scada/.venv/bin/activate && \
    cd /scada/hat-quickstart/playground/run && \
    ./system.sh 

#python3 client.py && \
