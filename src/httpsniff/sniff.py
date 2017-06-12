#!/usr/bin/env python
import os, sys
from scapy.all import *
from scapy.layers import http
from pprint import pprint
import paho.mqtt.publish as publish
import socket
import argparse
import pickle

MQTT_TOPIC="sitm/http"
portlist = [53, 80, 443]
destinations = {}

class SITMMPacket(object):

    def __init__(self, packet):
        ip = packet.getlayer(IP)
        self.src = ip.fields['src']
        self.dst = ip.fields['dst']
        self.type = 'unknonwn'

        if packet.haslayer(TCP):
            self.setvalues(packet.getlayer(TCP))
            self.type = 'tcp'

        if packet.haslayer(UDP):
            self.setvalues(packet.getlayer(UDP))
            self.type = 'udp'

    def __getstate__(self):
        pass

    def setvalues(self, layer):
        self.sport = layer.fields['sport']
        self.dport = layer.fields['dport']

def collect_data(dst, dport, host = None, path = None, ):
    if not destinations.has_key(dst):
        destinations[dst] = {dport: 1}
        return

    if not destinations[dst].has_key(dport):
        destinations[dst][dport] = 1
        return

    destinations[dst][dport] += 1
    return

def print_data():
    print
    for dst in destinations.keys():
        try:
            name, aliases, ip = socket.gethostbyaddr(dst)
        except Exception:
            name = 'unknown'
            aliases = []
            ip = dst
        print('##################################################')
        print('Destination Address: {}'.format(dst))
        print('Destination Name:    {}'.format(name))
        if len(aliases) > 0:
            print('Destination Aliases: '),
            for alias in aliases:
                print('{}, '),
            print
        print
        print('Port: Connection Count')
        for dport in destinations[dst].keys():
            print('{:4}: {:4}'.format(dport, destinations[dst][dport]))
        print
    print '```'

def handle_http_capture(src, dst, sport, dport, host, method, path):
    collect_data(dst, dport)
    msg = '{src}:{sport} -> {dst}:{dport} {method} {host}{path}'.format(src=src, dst=dst, sport=sport, dport=dport, host=host, method=method, path=path)
    print msg
    # publish.single(topic=MQTT_TOPIC, payload=msg)

def handle_capture(src, dst, sport, dport):
    if dport not in portlist:
        return
    collect_data(dst, dport)
    msg = '{src}:{sport} -> {dst}:{dport}'.format(src=src, dst=dst, sport=sport, dport=dport)
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

def print_tcp_packet(packet):
    tcp = packet.getlayer(TCP)
    ip = packet.getlayer(IP)
    if tcp.fields['dport'] not in portlist:
        return None

    msg = 'TCP {src}:{sport} -> {dst}:{dport}'.format(
            src=ip.fields['src'],
            dst=ip.fields['dst'],
            sport=tcp.fields['sport'],
            dport=tcp.fields['dport'],
            )
    return msg

def print_udp_packet(packet):
    udp = packet.getlayer(UDP)
    ip = packet.getlayer(IP)
    if udp.fields['dport'] not in portlist:
        return None

    msg = 'UDP {src}:{sport} -> {dst}:{dport}'.format(
            src=ip.fields['src'],
            dst=ip.fields['dst'],
            sport=udp.fields['sport'],
            dport=udp.fields['dport'],
            )
    return msg

def print_packet(packet):
    if packet.haslayer(TCP):
        return print_tcp_packet(packet)

    if packet.haslayer(UDP):
        return print_udp_packet(packet)

def process_packet(packet):
    ip_layer = packet.getlayer(IP)
    if not ip_layer:
        return

    d = packet2dict(packet)
    if not d:
        return
    packet_list.append(d)
    msg = print_packet(packet)
    if msg:
        print msg

def packet2dict(packet):
    d = {}
    ip = packet.getlayer(IP)
    d['src'] = ip.fields['src']
    d['dst'] = ip.fields['dst']
    d['http'] = None

    if packet.haslayer(TCP):
        layer = packet.getlayer(TCP)
        d['type'] = 'tcp'
        if packet.haslayer(http.HTTPRequest):
            d['http'] = True
            request = packet.getlayer(http.HTTPRequest)
            d['method'] = request.fields['Method']
            d['path'] = request.fields['Path']
            d['host'] = request.fields['Host']
    elif packet.haslayer(UDP):
        layer = packet.getlayer(UDP)
        d['type'] = 'udp'
    else:
        return None

    d['sport'] = layer.fields['sport']
    d['dport'] = layer.fields['dport']
    return d

if __name__ == '__main__':

    if not os.geteuid() == 0:
        sys.exit("\nPlease run this script as root, thanks.\n")
    packet_list = []
    parser = argparse.ArgumentParser(description = 'sniff network')
    parser.add_argument('output', help='path-to-output-file')
    args = parser.parse_args()

    sniff(iface='wlan0', filter='udp or tcp', prn=process_packet)
    pickle.dump(packet_list, open(args.output, 'wb'))
