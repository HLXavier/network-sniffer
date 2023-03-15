from socket import socket, AF_PACKET, SOCK_RAW, ntohs
from binascii import hexlify
from protocols import ARP, IPV4, IPV6, ARP_TYPES, NETWORK_PROTOCOLS, ICMP_TYPES, ICMPV6_TYPES, TRANSPORT_PROTOCOLS, ICMP, ICMPV6, UNDEFINED_PROTOCOL


def format_packet(raw_packet):
    packet = hexlify(raw_packet).decode("utf-8")
    return [packet[i:i+2] for i in range(0, len(packet), 2)]


def sizes(packets):
    packet_sizes = [len(packet) for packet in packets]

    min_size = min(packet_sizes) 
    max_size = max(packet_sizes)
    mean_size = sum(packet_sizes) / len(packet_sizes)

    return min_size, max_size, mean_size


# TODO
def handle_application(packet):
    return UNDEFINED_PROTOCOL


# TODO
def handle_tcp(packet):
    return UNDEFINED_PROTOCOL


# TODO
def handle_upd(packet):
    return UNDEFINED_PROTOCOL


def handle_arp(packet):
    bytes = ''.join(packet[6:8])

    if bytes in ARP_TYPES:
        return [ARP_TYPES[bytes]]

    return UNDEFINED_PROTOCOL


def handle_icmp(packet):
    bytes = packet[0]

    if bytes in ICMP_TYPES:
        return [ICMP_TYPES[bytes]]

    return UNDEFINED_PROTOCOL


def handle_ipv4(packet):
    ipv4_header = packet[:20]
    packet = packet[20:]

    bytes = ipv4_header[9]

    if bytes in TRANSPORT_PROTOCOLS:
        protocol = TRANSPORT_PROTOCOLS[bytes]

        if protocol == ICMP:
            return [protocol, *handle_icmp(packet)] 

        return [TRANSPORT_PROTOCOLS[bytes]]

    return UNDEFINED_PROTOCOL
    

def handle_icmpv6(packet):
    bytes = packet[0]

    if bytes in ICMPV6_TYPES:
        return [ICMPV6_TYPES[bytes]]

    return UNDEFINED_PROTOCOL


def handle_ipv6(packet):
    ipv6_header = packet[:40]
    packet = packet[40:]

    bytes = ipv6_header[6]

    if bytes in TRANSPORT_PROTOCOLS:
        protocol = TRANSPORT_PROTOCOLS[bytes]

        if protocol == ICMPV6:
            return [protocol, *handle_icmpv6(packet)]
        
        return [protocol]

    return UNDEFINED_PROTOCOL
        

def handle_network(packet):
    ethernet_header = packet[:14]
    packet = packet[14:]

    bytes = ''.join(ethernet_header[12:14])

    if bytes in NETWORK_PROTOCOLS:
        protocol = NETWORK_PROTOCOLS[bytes]

        if protocol == ARP:
            return [ARP, *handle_arp(packet)]
            
        if protocol == IPV4:
            return [IPV4, *handle_ipv4(packet)]

        if protocol == IPV6:
            return [IPV6, *handle_ipv6(packet)]


def process_packet(raw_packet):
    packet = format_packet(raw_packet)
    protocols = handle_network(packet)
    
    if protocols:
        print(protocols)


raw_socket = socket(AF_PACKET, SOCK_RAW, ntohs(3))

while True:
    raw_packet = raw_socket.recv(65535)
    process_packet(raw_packet)
