
from pathlib import Path
from typing import Self
from Atypes import Assignment, Student, TestResult


class StoreGradesToFile:
    def __init__(self, assignment: Assignment, file: Path):
        self.assignment = assignment
        self.file = file
        self.f = None

    def __enter__(self) -> Self:
        self.f = open(self.file, "w")
        self.f.write("Student | Passing | Erroring | Failing\n")
        return self

    def __exit__(self, *args):
        if self.f:
            self.f.close()


    def store_grade(self, student: Student, test_results: list[TestResult]):
        f = self.f
        if f:
            for test_result in test_results:
                f.write(f"{student.name} {test_result.passing} {test_result.erroring} {test_result.failing}\n")
                f.write("Erroring\n")
                for erroring in test_result.erroring_tests:
                    f.write("\t" + str(erroring) + "\n")
                f.write("Failing\n")
                for failing in test_result.failing_tests:
                    f.write("\t" + str(failing) + "\n")
        if f:
            f.flush()
