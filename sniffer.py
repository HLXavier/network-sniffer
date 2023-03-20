from socket import socket, AF_PACKET, SOCK_RAW, ntohs
from binascii import hexlify
from protocols import *
from stats import *
from os import system


def format_packet(raw_packet):
    packet = hexlify(raw_packet).decode("utf-8")
    return [packet[i:i+2] for i in range(0, len(packet), 2)]


def handle_application(from_port, to_port):
    if from_port in APPLICATION_PROTOCOLS:
        return [APPLICATION_PROTOCOLS[from_port]]

    if to_port in APPLICATION_PROTOCOLS:
        return [APPLICATION_PROTOCOLS[to_port]]

    return UNDEFINED_PROTOCOL


def handle_tcp(packet):
    data_offset = packet[12][0]
    header_size = int(data_offset, 16) * 4

    tcp_header = packet[:header_size]
    packet = packet[header_size:]
    
    from_bytes = ''.join(tcp_header[0:2])
    to_bytes = ''.join(tcp_header[2:4])
    from_port = int(from_bytes, 16)
    to_port = int(to_bytes, 16)

    return [f'from_port:{str(from_port)}', f'to_port:{str(to_port)}', *handle_application(from_port, to_port)]


def handle_udp(packet):
    udp_header = packet[:8]
    packet = packet[8:]

    from_bytes = ''.join(udp_header[0:2])
    to_bytes = ''.join(udp_header[2:4])
    from_port = int(from_bytes, 16)
    to_port = int(to_bytes, 16)

    return [f'from_port:{from_port}', f'to_port:{to_port}', *handle_application(from_port, to_port)]


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

        if protocol == TCP:
            return [protocol, *handle_tcp(packet)]

        if protocol == UDP:
            return [protocol, *handle_udp(packet)]

        if protocol == ICMP:
            return [protocol, *handle_icmp(packet)] 

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

        if protocol == TCP:
            return [protocol, *handle_tcp(packet)]

        if protocol == UDP:
            return [protocol, *handle_udp(packet)]

        if protocol == ICMPV6:
            return [protocol, *handle_icmpv6(packet)]

    return UNDEFINED_PROTOCOL
        

def handle_network(packet):
    ethernet_header = packet[:14]
    packet = packet[14:]

    bytes = ''.join(ethernet_header[12:14])

    if bytes in NETWORK_PROTOCOLS:
        protocol = NETWORK_PROTOCOLS[bytes]
        
        if protocol == ARP:
            return [protocol, *handle_arp(packet)]
            
        if protocol == IPV4:
            return [protocol, *handle_ipv4(packet)]

        if protocol == IPV6:
            return [protocol, *handle_ipv6(packet)]

    return UNDEFINED_PROTOCOL


def process_packet(raw_packet):
    packet = format_packet(raw_packet)
    protocols = handle_network(packet)

    ingest_raw_packet(raw_packet)
    ingest_stack(protocols)


raw_socket = socket(AF_PACKET, SOCK_RAW, ntohs(3))


i = 0
while True:
    raw_packet = raw_socket.recv(65535)
    process_packet(raw_packet)

    if i > 5:
        i = 0
        system('clear')   
        print_stats()

    i += 1