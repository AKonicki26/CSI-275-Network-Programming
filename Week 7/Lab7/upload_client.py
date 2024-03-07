"""Don't forget your docstring!"""

import argparse
import socket
import os
import constants


class UploadError(Exception):
    """Error when uploading."""

    pass


class UploadClient:
    # TODO document this class and implement the specified functions

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((host, port))

    def upload_file(self, file_path):
        """Upload a file to the class's server.

        The function handles Q4 of the original assignment.
        """
        # Open the file
        file = open(file_path, "rb")

        # Read the whole thing into memory
        file_data = file.read()

        # Prep the first line to send
        header = "UPLOAD " + os.path.basename(file_path) + " " \
                 + str(len(file_data)) + "\n"
        print(f"Sending {header}")

        self.tcp_sock.sendall(header.encode("ascii"))

        # Send the file data
        self.tcp_sock.sendall(file_data)

        # Wait for a response
        return_msg = self.recv_until_delimiter(b"\n").decode("ascii")
        if return_msg == "ERROR":
            raise UploadError
        else:
            print("Upload successful")

    def close(self):
        """Close the tcp socket."""
        self.tcp_sock.close()

    def recv_all(self, length: int) -> bytearray:
        data = b''
        while len(data) < length:
            more = self.tcp_sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more
        return data



    def recv_until_delimiter(self, delimiter, buffer):
        total_data = ''

        # TODO: Move this to where it's actually needed to be

        delimiter = "\n"
        buffer = "Hello\nSomethi\nng\n"

        if delimiter in buffer:
            print("Message found in the buffer")
            buffer = buffer[buffer.index(delimiter) + 1:]
            return total_data, buffer

        delim_not_found = True
        while delim_not_found:
            data = self.tcp_sock.recv(constants.MAX_BYTES).decode('utf-8')
            if delimiter in data:
                total_data += data[:len(data) - len(delimiter)]
                break
            total_data += data
            # Keep receiving data

        print(total_data)

    def list_files(self) -> list:
        self.tcp_sock.sendall("LIST\n".encode('utf-8'))
        self.recv_until_delimiter("\n")

        return []


    def bufferThing(self):



def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    parser = argparse.ArgumentParser(description="TCP File Uploader")
    parser.add_argument("host", help="interface the server listens at;"
                        " host the client sends to")
    parser.add_argument("-p", metavar="PORT", type=int,
                        default=constants.UPLOAD_PORT,
                        help=f"TCP port (default {constants.UPLOAD_PORT})")
    args = parser.parse_args()
    upload_client = UploadClient(args.host, args.p)
    upload_client.upload_file("upload_client.py")
    print(upload_client.list_files())
    upload_client.close()


if __name__ == "__main__":
    main()

