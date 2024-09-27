from ..project_validator_I import ProjectValidator_I
from ..project_validation_exception import ProjectValidationException
from ..project_I import Project_I
from os.path import dirname
from pathlib import Path
from .project_impl import EclipseMavenProject

class EclipseMavenProjectValidator(ProjectValidator_I):
    def zip_contains_project(self, files: list[str]):
        """
        If subclass doesn't care about zipfiles, always return true

        Populated with output of zip_file.namelist()
        """
        self.__is_project(files)

    def __is_project(self, files: list[str]) -> Path:
        """Returns root of project"""
        dot_project_files = [x for x in files if '.project' == Path(x).name]
        dot_classpath_files = [x for x in files if '.classpath' == Path(x).name]
        pom_files = [x for x in files if 'pom.xml' == Path(x).name]
        dot_settings_files = [x for x in files if '.settings' == Path(x).name]

        # One of each file and correct type
        error = ''
        if len(dot_project_files) != 1:
            error += f'Expected 1 .project file but found {len(dot_project_files)}\n'
        if len(dot_classpath_files) != 1:
            error += f'Expected 1 .classpath file but found {len(dot_classpath_files)}\n'
        if len(pom_files) < 1:
            error += f'Expected 1 pom.xml file but found 0\n'
        if len(dot_settings_files) != 1:
            error += f'Expected 1 .settings/ directory but found {len(dot_settings_files)}\n'
        elif not dot_settings_files[0].endswith('/'):
            error += f'Expected 1 .settings/ directory but found .settings/ file\n'
        
        if error:
            raise ProjectValidationException(error)

        dot_project = Path(dot_project_files[0])
        dot_classpath = Path(dot_classpath_files[0])
        pom = Path(pom_files[0])
        dot_settings = Path(dot_settings_files[0])

        # All config files at the same level
        if dirname( dot_project ) != dirname( dot_classpath ) \
        or dirname( pom ) != dirname( dot_settings) \
        or dirname( dot_project ) != dirname( pom ):
            raise Exception('Config files are not all at same level')
        return Path( dirname( dot_project ) )


    def is_project(self, directory_root: Path) -> Path:
        """
        Raises ProjectInstallException if is not a project

        :return: Project root or None if there is no enclosing directory
        """
        namelist: list[str] = []
        for x in directory_root.walk():
            path, dirs, files = x
            for dir in dirs:
                namelist.append( (path / dir ).as_posix() + '/' )
            for file in files:
                namelist.append( (path / file).as_posix() )
        return self.__is_project(namelist)

    def to_project(self, project_root: Path) -> 'Project_I':
        return EclipseMavenProject.create(project_root)