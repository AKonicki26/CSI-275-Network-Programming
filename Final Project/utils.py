import json
import socket
from constants import *


def recv_all(sock, length):
    """Receive specified amount of data from the socket"""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(
                'expected %d bytes but only received %d bytes before the socket closed' % (length, len(data)))
        data += more
    return data


def receive_message(sock: socket.socket) -> dict:
    message_size = int.from_bytes(sock.recv(4), "big")
    message = json.loads(recv_all(sock, message_size).decode(ENCODING))

    return message
