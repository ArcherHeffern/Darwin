from typing import Optional, Self
from models.backend_models import Student


class StudentFilterer:

    LEXICOLGRAPHIC_MIN = ""
    LEXICOLGRAPHIC_MAX = "{{{{{{{{{{"

    def __init__(self):
        self.__first_name_begin = self.LEXICOLGRAPHIC_MIN
        self.__first_name_end = self.LEXICOLGRAPHIC_MAX
        self.__last_name_begin = self.LEXICOLGRAPHIC_MIN
        self.__last_name_end = self.LEXICOLGRAPHIC_MAX

    def filter_first_name(self, begin: Optional[str], end: Optional[str]) -> Self:
        if begin:
            self.__first_name_begin = begin.lower()
        if end:
            self.__first_name_end = end.lower()
        return self

    def __filter_first_name(self, student: Student) -> bool:
        return (
            self.__first_name_begin
            <= student.name_tokens[0].lower()
            <= self.__first_name_end
        )

    def filter_last_name(self, begin: Optional[str], end: Optional[str]) -> Self:
        if begin:
            self.__last_name_begin = begin.lower()
        if end:
            self.__last_name_end = end.lower()
        return self

    def __filter_last_name(self, student: Student):
        # Student does not have a last name
        return (
            len(student.name_tokens) == 1
            or self.__last_name_begin
            <= student.name_tokens[-1].lower()
            <= self.__last_name_end
        )

    def filter(self, students: list[Student]) -> list[Student]:
        filtered_students = filter(self.__filter_first_name, students)
        filtered_students = filter(self.__filter_last_name, filtered_students)
        return list(filtered_students)
