from abc import abstractmethod
from typing import Self
from pathlib import Path

class Project_I:
    """This may only be instantiated via the 'to_project' method of project_validator_impl"""

    @classmethod
    @abstractmethod
    def create(cls, project_root: Path) -> Self|None:
        raise NotImplementedError

    @abstractmethod
    def build(self):
        raise NotImplementedError
    
    @abstractmethod
    def setup(self):
        """May move files around for better testing"""
        raise NotImplementedError
    
    @abstractmethod
    def get_tests(self):
        raise NotImplementedError
    
    @abstractmethod
    def run_tests(self):
        raise NotImplementedError

