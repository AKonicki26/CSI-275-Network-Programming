"""Don't forget your docstring!"""

import socket

HOST = "localhost"
PORT = 20000


class SortServer:
    """Don't forget your docstring!"""

    def __init__(self, host, port):
        "Don't forget your docstring!"
        self.server = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server.bind((host, port))

    @staticmethod
    def get_return_string(data: bytes) -> str:
        data = data.decode('ascii')
        if "LIST " not in data:
            return "ERROR"
        data_to_sort = data.split("LIST ")[1].split()

        def number_sort(num_list: list[str], descending = False) -> str:
            """Get the return string from list of numbers."""
            try:
                num_list = sorted([float(number) for number in num_list], reverse=descending)
                num_list = [(int(number) if int(number) == number
                             else float(number)) for number in num_list]
                return ("SORTED " +
                        str.join(" ",
                                 [str(num) for num in num_list]))
            except ValueError:
                return "ERROR"

        def string_sort(string_list: list[str], descending: False) -> str:
            if any([number for number in string_list if not number.isdigit()]):
                return "ERROR"
            return "SORTED " + str.join(" ", sorted(string_list, reverse=descending))


        return string_sort(data_to_sort)

    def run_server(self):
        """Don't forget your docstring!"""
        self.server.listen(20)

        while True:
            print("Waiting")
            client_socket, address = self.server.accept()

            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                client_socket.sendall(
                    self.get_return_string(data).encode('ascii'))


if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()
