from sqlite3 import Connection


class SubmissionDal:
    def __init__(self, c: Connection):
        self.c = c
