from typing import Optional, Self
from darwin.models.client_models import MoodleStudent


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

    def __filter_first_name(self, student: MoodleStudent) -> bool:
        first_name = student.name.lower().split()[0]
        return (
            self.__first_name_begin
            <= first_name
            <= self.__first_name_end
        )

    def filter_last_name(self, begin: Optional[str], end: Optional[str]) -> Self:
        if begin:
            self.__last_name_begin = begin.lower()
        if end:
            self.__last_name_end = end.lower()
        return self

    def __filter_last_name(self, student: MoodleStudent):
        # Student does not have a last name
        name_tokens = student.name.lower().split()
        if len(name_tokens) < 2:
            return False
        last_name = name_tokens[-1]
        return (
            self.__last_name_begin
            <= last_name
            <= self.__last_name_end
        )

    def filter(self, students: list[MoodleStudent]) -> list[MoodleStudent]:
        filtered_students = filter(self.__filter_first_name, students)
        filtered_students = filter(self.__filter_last_name, filtered_students)
        return list(filtered_students)
