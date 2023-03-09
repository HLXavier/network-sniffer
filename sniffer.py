from socket import socket, AF_PACKET, SOCK_RAW, ntohs


raw_socket = socket(AF_PACKET, SOCK_RAW, ntohs(3))
packets = [raw_socket.recv(65535) for _ in range(10)]







