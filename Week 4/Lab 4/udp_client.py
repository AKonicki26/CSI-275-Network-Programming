"""Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""

import socket
import constants
from random import randint

class TimeOutError(Exception):
    def __init__(self, message="An error occurred"):
        super().__init__(message)


class UDPClient:
    def __init__(self, host: str, port: int, include_id: bool = False):
        self.host = host
        self.port = port
        self.include_id = include_id

    def verify_response(self, message_id: str, response) -> str:
        """Verifies the message ID from a response containing one
        by checking the message ID against the ID in the response

        Returns the message after the | character if correct, otherwise returns an empty string"""

        #print("Received: " + response)
        if "|" not in response:
            return ""
        sections = response.split("|")
        if len(sections) != 2:
            return ""

        response_id = sections[0]
        response_character = sections[1]
        return response_character if str(message_id) == str(response_id) else ""


    def send_character(self, character: str) -> str:
        udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        wait_time = constants.INITIAL_TIMEOUT
        udp_conn.settimeout(wait_time)
        while wait_time <= constants.MAX_TIMEOUT:
            try:
                # If messages should be sent with a verification
                if self.include_id:
                    message_id = randint(0, constants.MAX_ID - 1)
                    #print(f"Sending: {message_id}|{character}")
                    udp_conn.sendto(f"{message_id}|{character}".encode('ascii'),
                                    (self.host, self.port))
                    response, address = udp_conn.recvfrom(constants.MAX_BYTES)
                    response = response.decode('ascii')

                    verify_response = self.verify_response(message_id, response)
                    if verify_response == "":
                        continue
                    return verify_response
                # If messages do not need a verification
                else:
                    #print("Sending: " + character)
                    udp_conn.sendto(character.encode('ascii'), (self.host, self.port))
                    response, address = udp_conn.recvfrom(constants.MAX_BYTES)
                    response = response.decode('ascii')
                    return response
            except socket.timeout:
                #print("Connection timed out")
                wait_time *= 2
                udp_conn.settimeout(wait_time)
        # Loop has exited, max wait time exceeded
        #print("Exceeded maximum wait time")
        raise TimeOutError()


    def send_message_by_character(self, message: str) -> str:
        return "".join([self.send_character(character) for character in message])


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
