import json
import socket
import threading
from time import sleep, strftime
from constants import *
from utils import *

class ClientData:
    user_id = ""


server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def print_message(message: dict):
    if message["type"] == "PRIVATE":
        print(f"[{strftime('%I:%M:%S %p')}] {message['sender']} whispers to you: {message['content']}")
    else:
        print(f"[{strftime('%I:%M:%S %p')}] {message['sender']}: {message['content']}")

def listening_loop():
    while True:
        message = receive_message(server_socket)
        print_message(message)

def sending_loop():
    while True:
        raw_message = input()

        if raw_message[0:2] == "/p":
            message_dict = {
                'type': "PRIVATE",
                'sender': ClientData.user_id,
                'recipient': raw_message.split()[1],
                'content': " ".join(raw_message.split()[2:])
            }
        elif raw_message == "EXIT":
            message_dict = {
                'type': "EXIT",
            }
        else:
            message_dict = {
                'type': "BROADCAST",
                'sender': ClientData.user_id,
                'content': raw_message
            }

        send_message(message_dict)

def send_message(message: dict):
    message_length = len(json.dumps(message)).to_bytes(4, 'big')
    message_to_send = message_length + json.dumps(message).encode(ENCODING)
    server_socket.sendall(message_to_send)


def connect_with_server():

    while ClientData.user_id == "":
        name = input("Hello! Please enter your user name: ")
        if name.isalnum():
            ClientData.user_id = name
        else:
            print("Invalid name: name must be alphanumeric")

    start_message = {
        'type': 'START',
        'name': ClientData.user_id
    }

    print("Connecting to server...")
    server_socket.connect(SERVER_ADDRESS)
    send_message(start_message)

    threading.Thread(target=listening_loop).start()
    threading.Thread(target=sending_loop).start()


if __name__ == "__main__":
    # Sleep for half a second, just to ensure the server starts before clients connect

    sleep(0.5)
    connect_with_server()
