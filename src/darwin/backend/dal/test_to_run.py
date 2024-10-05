from sqlite3 import Connection


class TestToRunDal:
    def __init__(self, c: Connection):
        self.c = c
