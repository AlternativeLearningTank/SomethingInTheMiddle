import os, sys
import time
import datetime
from pprint import pprint
import netaddr
from scapy.all import *
from scapy.layers import http
from intercept import *
import paho.mqtt.publish as publish

class HttpRequestIntercepted:
    def __init__(self, opts):
        self.options = opts
        self.ipsrc = None
        self.ipdst = None
        self.host  = None
        self.port  = None
        self.method  = None
        self.path  = None
    
    def __str__(self):
        return '{0.ipsrc} -> {0.ipdst}:{0.port} {0.method} {0.host}{0.path}'.format(self)

    @staticmethod
    def parse(pkt):
        tcp  = pkt.getlayer(TCP)
        ip   = pkt.getlayer(IP)
        req  = pkt.getlayer(http.HTTPRequest)

        reqi = HttpRequestIntercepted()
        reqi.ipsrc = ip.fields['src']
        reqi.ipdst = ip.fields['dst']
        reqi.port  = tcp.fields['dport']
        reqi.host  =  req.fields['Host']
        reqi.method = req.fields['Method'] 
        reqi.path  = req.fields['Path']
        
        return reqi

    def publish(self):
        msg = str(self)
        print("HTTP >>> " + msg)
        publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)

class HttpScanner:
    def __init__(self, wl=[80, 8080]):
        self.packets = []
        self.last = None
        self.whitelist = wl
 
    def process(self, pkt):
        if pkt.haslayer(http.HTTPRequest):
            self.last = HttpRequestIntercepted.parse( pkt )
            self.packets.append(self.last)
    
    def count(self):
        return len(self.packets)


# def handle_http_capture(src, dst, sport, dport, host, method, path):
#     collect_data(dst, dport)
#     msg = '{src}:{sport} -> {dst}:{dport} {method} {host}{path}'.format(src=src, dst=dst, sport=sport, dport=dport, host=host, method=method, path=path)
#     print msg
#     # publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)

# def handle_capture(src, dst, sport, dport):
#     if dport not in portlist:
#         return
#     collect_data(dst, dport)
#     msg = '{src}:{sport} -> {dst}:{dport}'.format(src=src, dst=dst, sport=sport, dport=dport)
#     print msg
#     # publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)

# def process_http_packet(packet):
#     '''
#     Processes a TCP packet, and if it contains an HTTP request, it prints it.
#     '''
#     layer3 = packet.getlayer(TCP)
#     if not layer3:
#         layer3 = packet.getlayer(UDP)
#         if not layer3:
#             return

#     ip_layer = packet.getlayer(IP)
#     if not ip_layer:
#         return
#     try:
#         if packet.haslayer(http.HTTPRequest):
#             request = packet.getlayer(http.HTTPRequest)
#             handle_http_capture(ip_layer.fields['src'], ip_layer.fields['dst'], layer3.fields['sport'], layer3.fields['dport'], request.fields['Host'], request.fields['Method'], request.fields['Path'])
#         else:
#             handle_capture(ip_layer.fields['src'], ip_layer.fields['dst'], layer3.fields['sport'], layer3.fields['dport'])

#     except KeyError as ke:
#         print 'KeyError: {}'.format(ke)
#         return

# def print_tcp_packet(packet):
#     tcp = packet.getlayer(TCP)
#     ip = packet.getlayer(IP)
#     if tcp.fields['dport'] not in portlist:
#         return None

#     msg = 'TCP {src}:{sport} -> {dst}:{dport}'.format(
#             src=ip.fields['src'],
#             dst=ip.fields['dst'],
#             sport=tcp.fields['sport'],
#             dport=tcp.fields['dport'],
#             )
#     return msg

# def print_udp_packet(packet):
#     udp = packet.getlayer(UDP)
#     ip = packet.getlayer(IP)
#     if udp.fields['dport'] not in portlist:
#         return None

#     msg = 'UDP {src}:{sport} -> {dst}:{dport}'.format(
#             src=ip.fields['src'],
#             dst=ip.fields['dst'],
#             sport=udp.fields['sport'],
#             dport=udp.fields['dport'],
#             )
#     return msg
