from itertools import chain
from colorama import Style, Fore
from sys import stderr


def flatmap(func, *iterable):
    return chain.from_iterable(map(func, *iterable))


class Logger:
    def __init__(self, enabled: bool = True, name: str = ""):
        self.enabled = enabled
        if name:
            name = "[" + name + "] "
        self.name: str = name

    def log(self, s: str):
        if self.enabled:
            print(self.name + s)

    def error(self, s: str):
        if self.enabled:
            print(f"{Fore.RED}{self.name}{s}{Style.RESET_ALL}", file=stderr)
