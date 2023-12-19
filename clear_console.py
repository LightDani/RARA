from os import system, name


def clear_console():
    system("cls" if name == "nt" else "clear")
