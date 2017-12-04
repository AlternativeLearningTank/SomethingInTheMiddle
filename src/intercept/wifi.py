import os, sys
import time
import datetime
from pprint import pprint
import netaddr
from scapy.all import *
from scapy.layers import http

class WifiProbe:
    def __init__(self):
        self.tstamp = None
        self.ssid   = "unknown"
        self.mac    = None
        self.manufacturer = "unknown"
        self.rssi   = 0

    @staticmethod
    def parse(pkt):
        probe = WifiProbe()

        # determine preferred time format 
        # log_time = str(int(time.time()))
        # # if time_fmt == 'iso':
        probe.tstamp = datetime.datetime.now().isoformat()

        # append the mac address itself
        probe.mac = pkt.addr2

        # parse mac address and look up the organization from the vendor octets
        try:
            parsed_mac = netaddr.EUI(pkt.addr2)
            probe.manufacturer = parsed_mac.oui.registration().org
        except netaddr.core.NotRegisteredError, e:
            pass

        # include the SSID in the probe frame
        probe.ssid = pkt.info if pkt.info else "unknown"

        rssi_val = -(256-ord(pkt.notdecoded[-4:-3]))
        probe.rssi = rssi_val

        return probe

class WifiProbeScanner:
    """
    see: https://supportforums.cisco.com/t5/wireless-mobility-documents/802-11-frames-a-starter-guide-to-learn-wireless-sniffer-traces/ta-p/3110019#toc-hId--1447989924

    type    = 0     => management frame
    subtype = 4     => probe request
    subtype = 8     => beacon
    """
    def __init__(self):
        self.probes = dict()  # mac address is key to this dictionary
    
    def process(self, pkt):
        """
        see: https://github.com/ivanlei/airodump-iv/blob/master/airoiv/airodump-iv.py
        """
        if not pkt.haslayer(Dot11):
            return

        # we are looking for management frames with a probe subtype
        # if neither match we are done here
        if pkt.type != 0 or pkt.subtype != 0x04:
            return
    
        probe = WifiProbe.parse(pkt)

        # do we already have aprobe for that ssid?
        if probe.ssid and (not probe.ssid in self.probes):
            self.probes.append( probe )
