from Atypes import Student


class Storage_I:
    # Download to disk
    def store_course(self): ...

    def store_assignment(self): ...

    def store_scrape(self):
        """Contains students, zip urns, grades, etc"""
        ...

    def upload_grade(self, student: Student):
        raise NotImplementedError

    def upload_grades(self, students: list[Student]):
        raise NotImplementedError

    def load_grade(self, student: Student):
        raise NotImplementedError

    def load_grades(self, student: Student):
        raise NotImplementedError
