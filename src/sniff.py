#!/usr/bin/env python
import os, sys
import time
import datetime
from pprint import pprint
from scapy.all import *
from scapy.layers import http
from pprint import pprint
import paho.mqtt.publish as publish
import socket
from intercept import *

MQTT_TOPIC_HTTP="sitm/http"
MQTT_TOPIC_WIFI="sitm/wifi"

portlist = [53, 80, 443]
destinations = {}


if __name__ == '__main__':

    # root guard
    if not os.geteuid() == 0:
        sys.exit("\nPlease run this script as root, thanks.\n")

    # read capture options from commandline
    opts = ScannerOptions.parse()

    sniff(iface='mon0', prn=process_packet) #, filter='udp or tcp', prn=process_packet)
    #pickle.dump(packet_list, open(args.output, 'wb'))
