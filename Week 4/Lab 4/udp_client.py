"""Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)

Author: Anne Konicki
Class: CSI-275
Assignment: Lab 4: UDP Sockets
Certification of Authenticity:
I certify that this is entirely my own work,
except where I have given fully documented
references to the work of others.I understand the definition and
consequences of plagiarism and acknowledge that the assessor of this assignment
may, for the purpose of assessing this assignment :
-Reproduce this assignment and provide a copy to another member of
academic staff; and / or
- Communicate a copy of this assignment to a plagiarism checking service
which may then retain a copy of this assignment on its database for
the purpose of future plagiarism checking)
"""

import socket
import constants
from random import randint


class TimeOutError(Exception):
    """Exception for UDP Connector timing out."""

    def __init__(self, message: str = "An error occurred"):
        """Create an instance of TimeOutError.

        :argument message the custom exception message attached
        to the exception.
        """
        super().__init__(message)


class UDPClient:
    """Creates a UDP connector and sends messages to it."""

    def __init__(self, host: str, port: int, include_id: bool = False):
        """Create an instance of a UDP client.

        :argument host IP address to connect to.
        :argument port IP Address port to connect to.
        :argument include_id boolean value, should the connector
        send unique message ID's attached to the sent data.
        """
        self.host = host
        self.port = port
        self.include_id = include_id

    def verify_response(self, message_id: str, response) -> str:
        """Verify the response ID received from the server.

        Checks the response ID against the message ID sent.

        Returns the message after the | character if correct,
        otherwise returns an empty string.

        :argument message_id message ID that was sent with character.
        :argument response the decoded response from the udp connector.
        """
        if "|" not in response:
            return ""
        sections = response.split("|")
        if len(sections) != 2:
            return ""

        response_id = sections[0]
        response_character = sections[1]
        return response_character if \
            str(message_id) == str(response_id) else ""

    def send_character(self, character: str) -> str:
        """Send an individual character to the instances UDP connection.

        :argument character the character to be sent.
        """
        udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        wait_time = constants.INITIAL_TIMEOUT
        udp_conn.settimeout(wait_time)
        while wait_time <= constants.MAX_TIMEOUT:
            try:
                # If messages should be sent with a verification
                if self.include_id:
                    message_id = randint(0, constants.MAX_ID - 1)
                    udp_conn.sendto(
                        f"{message_id}|{character}".encode('ascii'),
                        (self.host, self.port))
                    response, address = udp_conn.recvfrom(constants.MAX_BYTES)
                    response = response.decode('ascii')

                    verify_response = self.verify_response(message_id,
                                                           response)
                    if verify_response == "":
                        continue
                    return verify_response
                # If messages do not need a verification
                else:
                    udp_conn.sendto(character.encode('ascii'),
                                    (self.host, self.port))
                    response, address = udp_conn.recvfrom(constants.MAX_BYTES)
                    response = response.decode('ascii')
                    return response
            except socket.timeout:
                wait_time *= 2
                udp_conn.settimeout(wait_time)
        # Loop has exited, max wait time exceeded
        raise TimeOutError()

    def send_message_by_character(self, message: str) -> str:
        """Send a message to the UDP connection.

        Returns the message sent.

        :argument message The message to be sent
        """
        return "".join(
            [self.send_character(character) for character in message])


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
