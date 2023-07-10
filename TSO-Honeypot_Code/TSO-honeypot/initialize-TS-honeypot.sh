#!/bin/bash
# To be run after IMUNES experiment has started

echo "Configure packet forwarding for 10.0.0.0/16 over bridged connection (enp0s3) and host-only network (enp0s8)"
date

ip route add 10.0.0.0/16 via 10.0.2.1
sysctl -w net.ipv4.ip_forward=1

iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE 
iptables -A FORWARD -i enp0s3 -d 10.0.0.0/16 -m state --state RELATED,ESTABLISHED -j ACCEPT 
iptables -A FORWARD -s 10.0.0.0/16 -o enp0s3 -j ACCEPT


iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE 
iptables -A FORWARD -i enp0s8 -d 10.0.0.0/16 -m state --state RELATED,ESTABLISHED -j ACCEPT 
iptables -A FORWARD -s 10.0.0.0/16 -o enp0s8 -j ACCEPT


#hcp ./common/resolv.conf plc1:/etc/
hcp ./common/resolv.conf scada:/etc/

himage scada sysctl -w net.ipv4.conf.all.route_localnet=1

himage scada iptables -t nat -I PREROUTING -p tcp --dport 6514 -j DNAT --to 127.0.0.1:6514
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23010 -j DNAT --to 127.0.0.1:23010
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23011 -j DNAT --to 127.0.0.1:23011
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23012 -j DNAT --to 127.0.0.1:23012
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23020 -j DNAT --to 127.0.0.1:23020
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23021 -j DNAT --to 127.0.0.1:23021 # Hat Orchestrator
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23022 -j DNAT --to 127.0.0.1:23022 # Hat Monitor
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23023 -j DNAT --to 127.0.0.1:23023 # Hat GUI
himage scada iptables -t nat -I PREROUTING -p tcp --dport 23024 -j DNAT --to 127.0.0.1:23024 # Hat Manager

#firewall on router
himage router1 iptables -P FORWARD DROP
himage router1 iptables -A FORWARD -i eth0 -o eth2 -j ACCEPT
himage router1 iptables -A FORWARD -i eth2 -o eth1 -j ACCEPT
himage router1 iptables -A FORWARD -i eth3 -o eth1 -j ACCEPT
himage router1 iptables -A FORWARD -i eth2 -o eth3 -j ACCEPT
himage router1 iptables -I FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT


#docker exc/run podesiti tako umisto himage jer nema imunes komp kao base image 
echo "TS-honeypot initialized!"
date
