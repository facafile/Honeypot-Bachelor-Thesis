FROM siomiz/softethervpn 

COPY vpn_server.config /usr/vpnserver/vpn_server.config
COPY client.py client.py


ENV USERNAME=filip
ENV PASSWORD=test123
RUN apk add --no-cache python3 py3-pip

# Set up symlinks for convenience (optional)
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN if [ ! -e /usr/bin/pip ]; then ln -s /usr/bin/pip3 /usr/bin/pip; fi
RUN pip install watchdog

CMD /usr/bin/vpnserver execsvc && \
    python3 client.py

#CMD ["/usr/bin/vpnserver", "execsvc"]
#cmd dio kopiraj iz baznog NIJE OVO TRENUTNO!
#--env-file /path/to/envlist ovo mi je env variabla di su mi ove pizdarije

