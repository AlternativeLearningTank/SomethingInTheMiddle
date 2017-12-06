#!/usr/bin/env python
import os, sys
import time
import datetime
from pprint import pprint

from intercept import *
from intercept.wifi import *
from intercept.http import *

SCAN_PORTS = [53, 80, 443]

PktProcessor = None

def process_packet(pkt):
    PktProcessor.process( pkt )
    if PktProcessor.last:
	return PktProcessor.last.publish()

if __name__ == '__main__':
    # root guard
    if not os.geteuid() == 0:
        sys.exit("\nPlease run this script as root, thanks.\n")

    # read capture options from commandline
    opts = ScannerOptions.parse()

    print("sitm (cc) root@derfunke.net")
    print( "Begin scanning on interface '{0}'...".format(opts.iface) )
    print()

    if opts.type == 'wifi':
        PktProcessor=WifiProbeScanner()
        sniff(iface=opts.iface, prn=process_packet) #, filter='udp or tcp', prn=process_packet)
    elif opts.type == 'http':
        PktProcessor=HttpScanner(SCAN_PORTS)
        sniff(iface=opts.iface, filter='udp or tcp', prn=process_packet)
    else:
        print("Capture type not supported at the moment '", opts.type, "'")
