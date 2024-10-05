from abc import abstractmethod
from os import rmdir, getcwd, chdir
from typing import Self
from pathlib import Path
from models.backend_models import TestResult


class Project_I:
    """This may only be instantiated via the 'to_project' method of project_validator_impl"""

    def run(self, project_root: Path) -> TestResult:
        try:
            prev_dir = getcwd()
            chdir(project_root)

            self.clean()
            self.pre_compile_setup()
            self.compile_project()
            self.post_compile_setup()
            results: TestResult = self.run_tests()
            return results
        finally:
            chdir(prev_dir)

    @abstractmethod
    def clean(self):
        raise NotImplementedError

    @abstractmethod
    def pre_compile_setup(self):
        """
        Project type dependent setup
        """
        raise NotImplementedError

    @abstractmethod
    def post_compile_setup(self):
        """
        Project type dependent setup
        """
        raise NotImplementedError

    @abstractmethod
    def compile_project(self):
        """Does not compile test files"""
        raise NotImplementedError

    @abstractmethod
    def get_tests(self):
        raise NotImplementedError

    @abstractmethod
    def run_tests(self) -> TestResult:
        raise NotImplementedError
