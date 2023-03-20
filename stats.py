from protocols import *

stats = {}
port_stats = {}
packet_sizes = []


def ingest_raw_packet(packet):
    packet_sizes.append(len(packet))


def ingest_stack(protocol_stack):
    for entry in protocol_stack:
        if entry in stats:
            stats[entry] += 1
        else:
            stats[entry] = 1
    
        if entry and'to_port' in entry:
            port = entry.split(':')[1]
            port = int(port)
            if port in port_stats:
                port_stats[port] += 1
            else:
                port_stats[port] = 1
            


def print_stats():
    print_sizes()
    print_data_link_stats()
    print_network_stats()
    print_transport_stats()
    print_application_stats()


def print_sizes():
    min_size = min(packet_sizes) 
    max_size = max(packet_sizes)
    mean_size = sum(packet_sizes) / len(packet_sizes)

    print('Packet Sizes')
    print(f'min: {min_size}')
    print(f'max: {max_size}')
    print(f'mean: {mean_size}')


def print_network_stats():
    print('\nNetwork')
    print_stat(IPV4)
    print_stat(ICMP)
    print_stat(ICMPECHO_REQUEST)
    print_stat(ICMPECHO_REQUEST)
    print_stat(IPV6)
    print_stat(ICMPV6)
    print_stat(ICMPV6ECHO_REQUEST)
    print_stat(ICMPV6ECHO_REPLY)
    

def print_data_link_stats():
    print('\nData link')
    print_stat(ARP_REQUEST)
    print_stat(ARP_REPLY)


def print_transport_stats():
    print('\nTransport')
    print_stat(UDP)
    print_stat(TCP)

    sorted_ports = sorted(port_stats.items(), key=lambda port: port[1], reverse=True)
    top_ports = [port for port, _ in sorted_ports[:5]]
    print(f'Most used ports: {top_ports}')


def print_application_stats():
    print('\nApplication')
    print_stat(HTTP)
    print_stat(HTTPS)
    print_stat(DNS)
    print_stat(DHCP)
    print_stat(SSH)

def print_stat(protocol):
    count = get_count(protocol)
    percent = (count / len(packet_sizes)) * 100
    print(f'{protocol}: {percent:.2f}% ({count})')


def get_count(protocol):
    if protocol in stats:
        return stats[protocol]
    
    return 0
    