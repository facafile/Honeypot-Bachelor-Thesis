FROM imunes/vroot-process:latest

COPY client.py client.py

RUN pip install watchdog

CMD source /scada/.venv/bin/activate && \
    cd /scada/power-grid-simulator-master/ && \
    python -m simulator.main

#python3 client.py && \
