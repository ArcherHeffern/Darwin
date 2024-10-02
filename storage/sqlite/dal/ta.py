from sqlite3 import Connection


class TaDal:
    def __init__(self, c: Connection):
        self.c = c
