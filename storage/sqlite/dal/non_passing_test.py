from sqlite3 import Connection


class NonPassingTestDal:
    def __init__(self, c: Connection):
        self.c = c
