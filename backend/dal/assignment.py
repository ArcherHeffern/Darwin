from sqlite3 import Connection


class AssignmentDal:
    def __init__(self, c: Connection):
        self.c = c
