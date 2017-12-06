import os, sys
import time
import datetime
from pprint import pprint
import netaddr
from scapy.all import *
from scapy.layers import http
from intercept import *
import paho.mqtt.publish as publish

class WifiBeacon:
    def __init__(self):
        self.ssid   = "unknown"
        self.bssid   = "--"
        self.channel   = None
        self.mac    = None

    def __str__(self):
        return "{0.ssid}  {0.bssid}  {0.mac}".format(self)

    def publish(self):
        msg = str(self)
        print("802.11_beacon >>> " + msg)
        publish.single(topic=MQTT_TOPIC_WIFI_BEACON, payload=msg)

    @staticmethod
    def parse(pkt):
        beacon = WifiBeacon()

        beacon.ssid       = pkt[Dot11Elt].info
        beacon.bssid      = pkt[Dot11].addr3
        beacon.mac        = pkt.addr2
        beacon.channel    = int( ord(pkt[Dot11Elt:3].info))

        return beacon


class WifiProbe:
    def __init__(self):
        self.tstamp = None
        self.ssid   = "unknown"
        self.mac    = None
        self.manufacturer = "unknown"
        self.rssi   = 0
    
    def __str__(self):
        return "{0.tstamp}  {0.rssi}    {0.ssid}    {0.mac} {0.manufacturer}".format(self)

    def publish(self):
        msg = str(self)
        print("802.11_probe >>> " + msg)
        publish.single(topic=MQTT_TOPIC_WIFI_PROBE, payload=msg)

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
        self.beacons = dict()
        self.last = None
 
    def process(self, pkt):
        """
        see: https://github.com/ivanlei/airodump-iv/blob/master/airoiv/airodump-iv.py
        """

        # we are looking for management frames with a probe subtype
        # if neither match we are done here
        if pkt.haslayer(Dot11) and (pkt.type == 0):
            if (pkt.subtype == 0x04):
                probe = WifiProbe.parse(pkt)
                self.last = probe
                # # do we already have aprobe for that ssid?
                # if not self.probes.has_key(probe.ssid):
                #     self.probes.update( { probe.ssid : probe } )
                #     self.last = probe
            elif (pkt.subtype == 0x08):
                beacon = WifiBeacon.parse(pkt)
                self.last = beacon
                # # do we already have aprobe for that ssid?
                # if not self.beacons.has_key(beacon.ssid):
                #     self.beacons.update( { beacon.ssid : beacon } )
                #     self.last = beacon
            else:
                pass
        else:
            return

    def count(self):
        return (len(self.probes), len(self.beacons))


# def channel_hopper():
#     while True:
#         try:
#             channel = random.randrange(1,12)
#             os.system("iw dev %s set channel %d" % (interface, channel))
#             time.sleep(1)
#         except KeyboardInterrupt:
#             break
