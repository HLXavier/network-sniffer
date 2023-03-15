from socket import socket, AF_PACKET, SOCK_RAW, ntohs
from binascii import hexlify


def format_packet(raw_packet):
    packet = hexlify(raw_packet).decode("utf-8")
    return [packet[i:i+2] for i in range(0, len(packet), 2)]


def sizes(packets):
    packet_sizes = [len(packet) for packet in packets]

    min_size = min(packet_sizes) 
    max_size = max(packet_sizes)
    mean_size = sum(packet_sizes) / len(packet_sizes)

    return min_size, max_size, mean_size


def handle_arp(packet):
    opcode = ''.join(packet[6:8])

    if opcode == '0001':
        print('arp request')
    if opcode == '0002':
        print('arp reply')


def handle_ipv4(packet):
    icmp = '01'
    tcp = '06'
    udp = '11'

    protocols = {
        icmp: 'icmp',
        tcp: 'tcp',
        udp: 'udp',
    }

    ipv4_header = packet[:20]
    packet = packet[20:]

    bytes = ipv4_header[9]

    try:
        protocol = protocols[bytes]
    except:
        return None


def handle_icmpv6(packet):
    # Echo Request: Type 128
    # Echo Reply: Type 129
    type = packet[0]

    if type == '80':
        print('icmpv6 echo request')
    if type == '81':
        print('icmpv6 echo reply')


def handle_ipv6(packet):
    icmpv6 = '3a'
    tcp = '06'
    udp = '11'

    protocols = {
        icmpv6: 'icmpv6',
        tcp: 'tcp',
        udp: 'udp',
    }

    ipv6_header = packet[:40]
    packet = packet[40:]

    bytes = ipv6_header[6]

    try:
        protocol = protocols[bytes]
    except:
        return None

    if protocol == 'icmpv6':
        handle_icmpv6(packet)



def network(packet):
    arp = '0806'
    ipv4 = '0800'
    ipv6 = '86dd'

    protocols = {
        arp: 'arp',
        ipv4: 'ipv4',
        ipv6: 'ipv6',
    }

    ethernet_header = packet[:14]
    packet = packet[14:]

    bytes = ''.join(ethernet_header[12:14])

    try:
        protocol = protocols[bytes]
    except:
        return None
    
    # if protocol == 'arp':
    #     handle_arp(packet) 
        
    # if protocol == 'ipv4':
    #     handle_ipv4(packet) 

    if protocol == 'ipv6':
        handle_ipv6(packet)


def transport(packet):
    return []


def process_packet(raw_packet):
    packet = format_packet(raw_packet)
    protocols = network(packet)


raw_socket = socket(AF_PACKET, SOCK_RAW, ntohs(3))


while True:
    raw_packet = raw_socket.recv(65535)
    process_packet(raw_packet)
