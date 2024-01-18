def build_list() -> []:
    input = str('0')
    list = []
    print("Input things until you don't feel like it anymore, type 'Done' to stop")
    while True:
        user_input = input('Enter thing: ')
        if user_input == "done":
            break
        list.append(user_input)
    return list


def sort_list(list: []):
    print(list.sort())

if __name__ == "__main__":
    list = build_list()
    sort_list(list)
