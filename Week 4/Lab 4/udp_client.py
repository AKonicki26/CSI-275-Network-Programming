"""Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""

import socket
import constants

class UDPClient():
    def __init__(self, host: str, port: int, include_id: bool = False):
        self.host = host
        self.port = port
        self.include_id = include_id

    def send_message_by_character(self, message: str) -> str:
        udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        wait_time = constants.INITIAL_TIMEOUT
        udp_conn.settimeout(wait_time)
        while True: # While loop taken from slides, modified by Anne Konicki
            try:
                udp_conn.sendto(message.encode('ascii'), (self.host, self.port))
                response, address = udp_conn.recvfrom(constants.MAX_BYTES)
                return response.decode()
            except socket.timeout:
                print("Connection timed out")
                wait_time *= 2
                if wait_time >= constants.MAX_TIMEOUT:
                    print("Exceeded max wait time")
                    break
                udp_conn.settimeout(wait_time)
                # If we exceed our max wait time,
                # break the loop

def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
