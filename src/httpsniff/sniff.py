#!/usr/bin/env python
import os, sys
from scapy.all import *
from scapy.layers import http
from pprint import pprint
import paho.mqtt.publish as publish
import socket


MQTT_TOPIC="sitm/http"
portlist = [80]

def handle_http_capture(src, dst, sport, dport, host, method, path):
    msg = '{src}:{sport} -> {dst}:{dport} {method} {host}{path}'.format(src=src, dst=dst, sport=sport, dport=dport, host=host, method=method, path=path)
    print msg
    # publish.single(topic=MQTT_TOPIC, payload=msg)

def handle_capture(src, dst, sport, dport):
    if dport not in portlist:
        return
    try:
        name, a, i = socket.gethostbyaddr(dst)
    except Exception as e:
        name = 'unknown'
    msg = '{src}:{sport} -> {dst}:{dport} ({name})'.format(src=src, dst=dst, sport=sport, dport=dport, name=name)
    print msg
    # publish.single(topic=MQTT_TOPIC, payload=msg)

def process_http_packet(packet):
    '''
    Processes a TCP packet, and if it contains an HTTP request, it prints it.
    '''
    layer3 = packet.getlayer(TCP)
    if not layer3:
        layer3 = packet.getlayer(UDP)
        if not layer3:
            return

    ip_layer = packet.getlayer(IP)
    if not ip_layer:
        return
    try:
        if packet.haslayer(http.HTTPRequest):
            request = packet.getlayer(http.HTTPRequest)
            handle_http_capture(ip_layer.fields['src'], ip_layer.fields['dst'], layer3.fields['sport'], layer3.fields['dport'], request.fields['Host'], request.fields['Method'], request.fields['Path'])
        else:
            handle_capture(ip_layer.fields['src'], ip_layer.fields['dst'], layer3.fields['sport'], layer3.fields['dport'])

    except KeyError as ke:
        print 'KeyError: {}'.format(ke)
        return


if not os.geteuid() == 0:
    sys.exit("\nPlease run this script as root, thanks.\n")
# sniff(iface='wlan0', filter='tcp and ( port 80 or port 443 )', prn=process_http_packet)
sniff(iface='wlan0', filter='udp or tcp', prn=process_http_packet, store=0)
