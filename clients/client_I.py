from Atypes import Student
from abc import ABC, abstractmethod
from pathlib import Path

from clients.student_filterer import StudentFilterer


class Client_I(ABC):
    @abstractmethod
    def get_students(self, student_filterer: StudentFilterer) -> list[Student]:
        raise NotImplementedError

    @abstractmethod
    def install_file(self, url: str, destination: Path):
        raise NotImplementedError
