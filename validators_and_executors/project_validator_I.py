from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from .project_I import Project_I

class ProjectValidator_I(ABC):

    @abstractmethod
    def zip_contains_project(self, files: list[str]) -> bool:
        """
        If subclass doesn't care about zipfiles, always return true
        
        Raises ProjectInstallException if zipfile does not contain zipfile
        """
        raise NotImplementedError

    @abstractmethod
    def is_project(self, directory_root: Path) -> None:
        """Raises ProjectInstallException if is not a project"""
        raise NotImplementedError

    @abstractmethod
    def to_project(self, project_root: Path) -> Optional['Project_I']:
        raise NotImplementedError
    