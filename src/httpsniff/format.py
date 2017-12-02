#!/usr/bin/env python
import os, sys
# from scapy.all import *
# from scapy.layers import http
# from pprint import pprint
import socket
import argparse
import pickle
from sniff import SITMMPacket

def collect_data(packet):
    if not data.has_key(packet['dst']):
        data[packet['dst']] = {packet['dport']: 1}
        return

    if not data[packet['dst']].has_key(packet['dport']):
        data[packet['dst']][packet['dport']] = 1
        return

    data[packet['dst']][packet['dport']] += 1
    return

def print_data():
    print
    for dst in data.keys():
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
        for dport in data[dst].keys():
            print('{:4}: {:4}'.format(dport, data[dst][dport]))
        print
    print '```'

def process_http_packet(packet):
    msg = 'TCP/HTTP {dst}:{dport} {method} http://{host}{path}'.format(
            dst=packet['dst'],
            dport=packet['dport'],
            method=packet['method'],
            host=packet['host'],
            path=packet['path'],
            )
    return msg

def process_generic_packet(layer, packet):
    msg = '{layer} {src}:{sport} -> {dst}:{dport}'.format(
            layer=layer,
            src=packet['src'],
            dst=packet['dst'],
            sport=packet['sport'],
            dport=packet['dport'],
            )
    return msg

def process_tcp_packet(packet):
    if packet['dport'] not in portlist:
        return None

    if packet['http']:
        return process_http_packet(packet)

    return process_generic_packet('TCP', packet)

def process_udp_packet(packet):
    if packet['dport'] not in portlist:
        return None
    return process_generic_packet('UDP', packet)

def process_packet(packet):
    if packet['type'] == 'tcp':
        return process_tcp_packet(packet)

    if packet['type'] == 'udp':
        return process_udp_packet(packet)

def process_packets(packet_list):
    for packet in packet_list:
        msg = process_packet(packet)
        if msg:
            print msg
            collect_data(packet)

if __name__ == '__main__':

    if not os.geteuid() == 0:
        sys.exit("\nPlease run this script as root, thanks.\n")
    portlist = [53, 80, 443]
    data = {}
    parser = argparse.ArgumentParser(description = 'sniff network')
    parser.add_argument('input', help='path-to-input-file')
    args = parser.parse_args()

    print '### Something In The Middle, Maybe - Report\n```'
    process_packets(pickle.load(open(args.input, 'rb')))
    print_data()

