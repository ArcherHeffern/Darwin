from abc import ABC, abstractmethod
from pathlib import Path

class ProjectValidator_I(ABC):

    @abstractmethod
    def get_zip_project_root(self, files: list[str]) -> Path:
        """
        Raises ProjectInstallException if zipfile does not contain zipfile
        """
        raise NotImplementedError

    @abstractmethod
    def get_project_root(self, directory_root: Path) -> Path:
        """Raises ProjectInstallException if is not a project"""
        raise NotImplementedError
