# === Network Layer ===
ARP = 'arp'
ARP_REQUEST = 'arp_request'
ARP_REPLY = 'arp_reply'

IPV4 = 'ipv4'
IPV6 = 'ipv6'

NETWORK_PROTOCOLS = {
    '0806': ARP,
    '0800': IPV4,
    '86dd': IPV6
}

ARP_TYPES = {
    '0001': ARP_REQUEST,
    '0002': ARP_REPLY
}

# === Transport Layer ===
ICMP = 'icmp'
ICMPECHO_REQUEST = 'icmpecho_request'
ICMPECHO_REPLY = 'icmpecho_reply'

ICMPV6 = 'icmpv6'
ICMPV6ECHO_REQUEST = 'icmpv6echo_request' 
ICMPV6ECHO_REPLY = 'icmpv6echo_reply'

TCP = 'tcp'
UDP = 'udp'

TRANSPORT_PROTOCOLS = {
    '01': ICMP,
    '06': TCP,
    '11': UDP,
    '3a': ICMPV6
}

ICMP_TYPES = {
    '08': ICMPECHO_REQUEST,
    '00': ICMPECHO_REPLY
}

ICMPV6_TYPES = {
    '80': ICMPV6ECHO_REQUEST,
    '81': ICMPV6ECHO_REPLY
}

# === Application Layer ===
HTTP = 'http'
HTTPS = 'https'
DNS = 'dns'
DHCP = 'dhcp'
SSH = 'ssh'

APPLICATION_PROTOCOLS = {
    80: HTTP,
    443: HTTPS,
    53: DNS,
    68: DHCP,
    22: SSH
}

UNDEFINED_PROTOCOL = [None]
