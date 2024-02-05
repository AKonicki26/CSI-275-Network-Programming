import socket


def build_list() -> list:
    input_list = []
    print("Input things until you don't feel like it anymore, type 'Done' to stop")
    while True:
        user_input = input('Enter thing: ')
        if user_input.lower() == "done":
            break
        try:
            user_input = float(user_input)
            if int(user_input) == user_input:
                user_input = int(user_input)
            input_list.append(user_input)
        except ValueError as ex:
            print(f"Your inputs must be numbers!\n{type(ex).__name__}: {ex}")
        except Exception as ex:
            print(f"Something unexpected happened:\n{type(ex).__name__}: {ex}")
        # exception type from:
        # https://stackoverflow.com/questions/9823936/how-do-i-determine-what-type-of-exception-occurred

    return input_list


def sort_list(unsort_list: list) -> None:
    def encode(string: str) -> bytes:
        return string.encode('ascii')

    def decode(string: str) -> bytes:
        return string.decode('ascii')

    conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_info = ("68.183.63.165", 7778)
    conn.connect(server_info)

    send_string = "LIST " + str.join(" ", [str(element) for element in unsort_list])
    conn.sendall(encode(send_string))

    reply = conn.recv(4096)
    print(decode(reply))

    conn.close()


if __name__ == "__main__":
    unsorted_list = build_list()
    sort_list(unsorted_list)
