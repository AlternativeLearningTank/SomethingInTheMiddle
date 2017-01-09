#!/usr/bin/env python

# from http://www.lucainvernizzi.net/blog/2015/02/12/extracting-urls-from-network-traffic-in-just-9-python-lines-with-scapy-http/
# requires https://github.com/invernizzi/scapy-http
from scapy.all import IP, sniff
from scapy.layers import http
from pprint import pprint

def process_intercept(origin, dsthost, dstpath, dstmethod):
    print "*"*69
    print '\n{0} just requested a {1} {2}{3}'.format(origin, dstmethod, dsthost, dstpath)

def process_tcp_packet(packet):
    '''
    Processes a TCP packet, and if it contains an HTTP request, it prints it.
    '''
    if not packet.haslayer(http.HTTPRequest):
        # This packet doesn't contain an HTTP request so we skip it
        return
    http_layer = packet.getlayer(http.HTTPRequest)
    ip_layer = packet.getlayer(IP)
    #print "*"*69
    #pprint(ip_layer.fields)
    #pprint(http_layer.fields)
    process_intercept(ip_layer.fields['src'], http_layer.fields['Host'], http_layer.fields['Path'], http_layer.fields['Method'])

# Start sniffing the network.
sniff(iface='wlan0', filter='tcp port 80', prn=process_tcp_packet)
