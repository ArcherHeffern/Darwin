from sqlite3 import Connection


class GradingMetadataDal:
    def __init__(self, c: Connection):
        self.c = c
