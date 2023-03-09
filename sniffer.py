from socket import socket, AF_PACKET, SOCK_RAW, ntohs


def sizes(packets):
    packet_sizes = [len(packet) for packet in packets]

    min_size = min(packet_sizes) 
    max_size = max(packet_sizes)
    mean_size = sum(packet_sizes) / len(packet_sizes)

    return min_size, max_size, mean_size


raw_socket = socket(AF_PACKET, SOCK_RAW, ntohs(3))
packets = [raw_socket.recv(65535) for _ in range(10)]







