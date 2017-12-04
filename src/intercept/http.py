def handle_http_capture(src, dst, sport, dport, host, method, path):
    collect_data(dst, dport)
    msg = '{src}:{sport} -> {dst}:{dport} {method} {host}{path}'.format(src=src, dst=dst, sport=sport, dport=dport, host=host, method=method, path=path)
    print msg
    # publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)

def handle_capture(src, dst, sport, dport):
    if dport not in portlist:
        return
    collect_data(dst, dport)
    msg = '{src}:{sport} -> {dst}:{dport}'.format(src=src, dst=dst, sport=sport, dport=dport)
    print msg
    # publish.single(topic=MQTT_TOPIC_HTTP, payload=msg)

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
