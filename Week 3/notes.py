"""Network protocol is a social construct, it has predefined rules to follow
Mechanism for devices to identify and make connection with one another
Formatting rules that specify how data is packaged into messages
Rules on how those "packets" are sent received
    Packet is the fundamental unity of sharing among networking devices
    Data is wrapped in a packet before being sent"""

import socket


def to_bytestring(string: str) -> bytes:
    print(f'Receieved string "{string}"')
    byte_string = string.encode("utf-8")
    print(f'String as byte-string is "{byte_string}"')
    return byte_string


if __name__ == "__main__":
    # socket.AF_INET = IPv4
    # socket.AP_INET6 = IPv6

    # socket.SOCK_STREAM = TCP
    connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    server_data = ("google.com", 80)
    connection.connect(server_data)  # Requires a tuple
    connection.sendall(to_bytestring("Hello World"))  # Requires ByteString (the b before the quotes)

    # Google doesn't like us and doesn't respond :/
    # reply = connection.recv(4096)
    # print(f'Received reply from Google.com: {reply}')

    connection.close()  # Always close connection

    # Listening one this time!
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

    # Either "0.0.0.0" or "127.0.0.1", anything or only this computer respectively
    listen_address = ("0.0.0.0", 12000)
    listen_socket.bind(listen_address)

    # Open the port, so now information can come in
    listen_socket.listen()

    # Now we are ready to receive connections
    print('Awaiting data')
    conn_socket, conn_addr = listen_socket.accept()
    print(f'Received connection from {conn_addr}')

    # Now we follow out protocol
    # Receive a message from the client

    # From now on, we only use conn_socket
    # Listen socket is only for receiving, conn_socket is
    # What we actually connected to

    received_data = conn_socket.recv(4096)
    message = received_data.decode('ascii')
    print(f'Received message: {message}')

    # Close all connections
    conn_socket.close()
    listen_socket.close()
