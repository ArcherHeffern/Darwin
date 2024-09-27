from typing import Self
from pathlib import Path
from .dot_project import DotProject
from .dot_settings import DotSettings
from .dot_classpath import DotClasspath
from ..project_I import Project_I
from ..project_validation_exception import ProjectValidationException


class EclipseMavenProject(Project_I):
    def __init__(self, project_root: Path, dot_project: DotProject, dot_classpath: DotClasspath, dot_settings: DotSettings):
        self._project_root = project_root
        self._dot_project = dot_project
        self._dot_classpath = dot_classpath
        self._dot_settings = dot_settings

    @classmethod
    def create(cls, project_root: Path) -> Self:
        dot_project_file = project_root / '.project'
        dot_classpath_file = project_root / '.classpath'
        dot_settings_file = project_root / '.settings'

        if not dot_project_file.exists():
            raise ProjectValidationException('.project not found')
        if not dot_classpath_file.exists():
            raise ProjectValidationException('.classpath not found')
        if not dot_settings_file.exists():
            raise ProjectValidationException('.settings not found')

        dot_project = DotProject.create(dot_project_file)
        dot_classpath = DotClasspath.create(dot_classpath_file)
        dot_settings = DotSettings.create(dot_settings_file)
        return cls(project_root, dot_project, dot_classpath, dot_settings)

    def build(self):
        raise NotImplementedError
    
    def setup(self):
        """May move files around for better testing"""
        raise NotImplementedError
    
    def run_tests(self):
        raise NotImplementedError