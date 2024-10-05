from sqlite3 import Connection


class TestCaseDal:
    def __init__(self, c: Connection):
        self.c = c
