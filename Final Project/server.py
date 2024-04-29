import json
import random
import socket
import sys
import threading
from constants import *
from utils import *

class Server:
    def __init__(self, address: tuple):
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.clients = []

    def send_message_to_all(self, message_dict: dict):
        [client.send_message_to(message_dict) for client in self.clients]

    def send_message_to_user(self, message_dict: dict):
        print("Sending a message to " + message_dict['recipient'])
        [client.send_message_to(message_dict) for client in self.clients if client.user_id == message_dict['recipient']]

    def disconnect_user(self, user_id:str):
        print(self.clients)
        self.clients = [client for client in self.clients if client.user_id != user_id]
        print(self.clients)


server = Server(SERVER_ADDRESS)

class Client:
    def __init__(self, socket, ip_addr, name):
        self.socket = socket
        self.ip = ip_addr
        self.user_id = name

    def send_message_to(self, message: dict):
        json_message = json.dumps(message).encode(ENCODING)
        message_length = len(json_message).to_bytes(4, 'big')

        self.socket.sendall(message_length + json_message)

    def listening_thread(self):
        while True:
            print("awaiting message...")
            message = receive_message(self.socket)
            if message["type"] == "BROADCAST":
                server.send_message_to_all(message)
            elif message["type"] == "PRIVATE":
                server.send_message_to_user(message)
            elif message["type"] == "EXIT":
                server.disconnect_user(self.user_id)
            print(message)


def connect_to_client(sock: socket.socket, ip_addr: str):
    start_message = receive_message(sock)

    if start_message["type"] != "START":
        return

    client_id = start_message["name"]
    client = Client(sock, ip_addr, client_id)
    server.clients.append(client)

    return_message = {
        'type': "BROADCAST",
        'sender': "SERVER",
        'content': f"Welcome to the server, {client_id}!"
    }

    client.send_message_to(return_message)
    threading.Thread(target=client.listening_thread).start()


def start_accepting_connections():
    print("Creating server connection")

    Client.server_socket = server.sock
    print("Awaiting connections")
    server.sock.listen(20)

    while True:
        sock, addr = server.sock.accept()
        print("Found connection")
        threading.Thread(target=connect_to_client, args=(sock, addr)).start()


if __name__ == '__main__':
    start_accepting_connections()
