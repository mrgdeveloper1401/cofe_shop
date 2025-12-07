import os


def get_envbool(name: str, value: bool) -> bool:
    get_value = os.getenv(name, value)

    if get_value is None:
        return get_value
    if get_value and get_value.lower() == "false":
        return False
    if get_value and get_value.lower() == "true":
        return True
