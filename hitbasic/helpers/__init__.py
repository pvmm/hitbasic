def is_multiline(*statements):
    "find multiline statement in a group"
    for stmt in statements:
        if stmt.multiline:
            return True

        if stmt.group:
            return is_multiline(iter(stmt))

    return False


def debug(obj, caption=None, ignore_keys=['parent']):
    if caption:
        print(f"======={caption}=======")
    else:
        print("======={BEGIN}=======")

    for key, value in obj.__dict__.items():
        if not key in ignore_keys:
            print(f'{key} = {value}')
    print("======={END}=======")
