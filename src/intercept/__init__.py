from optparse import OptionParser

MQTT_TOPIC_HTTP="sitm/http"
MQTT_TOPIC_HTTP_IMG="sitm/http/img"
MQTT_TOPIC_WIFI_BEACON="sitm/wifi/beacon"
MQTT_TOPIC_WIFI_PROBE="sitm/wifi/probe"


class ScannerOptions:
	def __init__(self):
		self.iface = 'mon0'
		self.packet_count = 0
		self.channel = -1
		self.channel_hop = True
		self.max_channel = -1
		self.input_file = None
	
	@staticmethod
	def parse():
		parser = OptionParser()
		parser.add_option('-i', '--iface', dest='iface', default='mon0', help='Interface to bind to')
		parser.add_option('-t', '--type', dest='type', default='http', help='Type of capture [wifi, http, img]')
		opts, _ = parser.parse_args()
        return opts
		



"""
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
"""

# def collect_data(dst, dport, host = None, path = None, ):
#     if not destinations.has_key(dst):
#         destinations[dst] = {dport: 1}
#         return

#     if not destinations[dst].has_key(dport):
#         destinations[dst][dport] = 1
#         return

#     destinations[dst][dport] += 1
#     return

# def print_data():
#     print
#     for dst in destinations.keys():
#         try:
#             name, aliases, ip = socket.gethostbyaddr(dst)
#         except Exception:
#             name = 'unknown'
#             aliases = []
#             ip = dst
#         print('##################################################')
#         print('Destination Address: {}'.format(dst))
#         print('Destination Name:    {}'.format(name))
#         if len(aliases) > 0:
#             print('Destination Aliases: '),
#             for alias in aliases:
#                 print('{}, '),
#             print
#         print
#         print('Port: Connection Count')
#         for dport in destinations[dst].keys():
#             print('{:4}: {:4}'.format(dport, destinations[dst][dport]))
#         print
#     print '```'


# def print_packet(packet):
#     if packet.haslayer(Dot11):
#         return print_dot11_packet(packet)

#     if packet.haslayer(TCP):
#         return print_tcp_packet(packet)

#     if packet.haslayer(UDP):
#         return print_udp_packet(packet)

# def process_packet(packet):
#     if packet.haslayer(Dot11) or packet.haslayer(IP):
#         # d = packet2dict(packet)
#         # if not d:
#         #     return
#         # packet_list.append(d)
#         msg = print_packet(packet)
#         if msg:
#             print msg
#         # dispatch over MQTT
#         #publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)
#     else:
#         return
    
#     #ip_layer = packet.getlayer(IP)
#     #if not ip_layer:
#     #    return

# def packet2dict(packet):
#     d = {}
#     ip = packet.getlayer(IP)
#     d['src'] = ip.fields['src']
#     d['dst'] = ip.fields['dst']
#     d['http'] = None

#     if packet.haslayer(TCP):
#         layer = packet.getlayer(TCP)
#         d['type'] = 'tcp'
#         if packet.haslayer(http.HTTPRequest):
#             d['http'] = True
#             request = packet.getlayer(http.HTTPRequest)
#             d['method'] = request.fields['Method']
#             d['path'] = request.fields['Path']
#             d['host'] = request.fields['Host']
#     elif packet.haslayer(UDP):
#         layer = packet.getlayer(UDP)
#         d['type'] = 'udp'
#     else:
#         return None

#     d['sport'] = layer.fields['sport']
#     d['dport'] = layer.fields['dport']
#     return d
