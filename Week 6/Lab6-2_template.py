"""Don't forget your docstring!"""

import socket

HOST = "localhost"
PORT = 45000


class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """Create TCP socket and bind it to host and port"""
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((HOST, PORT))

    @staticmethod
    def recv_all(sock, length):
        """Receive specified amount of data from a socket."""
        data = b''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('expected %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more
        return data

    def calc_length(self):
        """Receive connections from client with length prefix.

        Get the prefix, then send the length of the actual received
        data back to the client"""
        self.connection.listen(20)
        while True:
            print("\nWaiting for connection")
            connection, address = self.connection.accept()

            length = int.from_bytes(connection.recv(4), "big")
            print(f"Message length is {length}")

            try:
                message = self.recv_all(connection, length).decode('ascii')
            except EOFError as ex:
                connection.sendall(len("Length Error").to_bytes(4, 'big') + "Length Error".encode('ascii'))
                print(f"Length Error:\n{type(ex).__name__}: {ex}")
            except Exception as ex:
                print(f"Unexpected error:\n{type(ex).__name__}: {ex}")

            # print(f"Message received: {message}")

            response = f"I received {len(message)} bytes."
            string_to_send = len(response).to_bytes(4, 'big') + response.encode('ascii')
            connection.sendall(string_to_send)

            connection.close()


if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()
