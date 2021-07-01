import datetime

def log(*message):
    """
    Logs messages by printing them and giving us the datetime.

    :param message: message we want to print
    """
    output = "" #basically allows us to print multiple messages smoothly
    for element in message:
        output += " "+element

    now = datetime.datetime.now().replace(microsecond=0)
    print(f"[{now}]: {output}")
