def build_list() -> []:
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


def sort_list(unsort_list: []):
    print(sorted(unsort_list))


if __name__ == "__main__":
    unsorted_list = build_list()
    sort_list(unsorted_list)
