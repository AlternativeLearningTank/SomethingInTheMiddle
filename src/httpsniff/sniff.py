#!/usr/bin/env python
import os, sys
from scapy.all import IP, sniff
from scapy.layers import http
from pprint import pprint
import paho.mqtt.publish as publish


MQTT_TOPIC="sitm/http"

def handle_capture(origin, dsthost, dstpath, dstmethod):
    msg = "\n{0} \t {1} {2}{3}".format(origin, dstmethod, dsthost, dstpath)
    print msg
    publish.single(topic=MQTT_TOPIC, payload=msg)

def process_http_packet(packet):
    '''
    Processes a TCP packet, and if it contains an HTTP request, it prints it.
    '''
    if not packet.haslayer(http.HTTPRequest):
        # This packet doesn't contain an HTTP request so we skip it
        return
    http_layer = packet.getlayer(http.HTTPRequest)
    ip_layer = packet.getlayer(IP)
    try:
        handle_capture(ip_layer.fields['src'], http_layer.fields['Host'], http_layer.fields['Path'], http_layer.fields['Method'])
    except KeyError as ke:
        pass


if not os.geteuid() == 0:
    sys.exit("\nPlease run this script as root, thanks.\n")

sniff(iface='wlan0', filter='tcp port 80', prn=process_http_packet)
