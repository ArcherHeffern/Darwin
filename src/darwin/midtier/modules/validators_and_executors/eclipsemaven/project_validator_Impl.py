from ..project_validator_I import ProjectValidator_I
from pprint import pprint
from models.backend_models import ProjectValidationException
from os.path import dirname
from pathlib import Path


class MavenProjectValidator(ProjectValidator_I):
    def get_zip_project_root(self, files: list[str]) -> Path:
        """
        If subclass doesn't care about zipfiles, always return true

        Populated with output of zip_file.namelist()
        """
        return self.__is_project(files)

    def __is_project(self, files: list[str]) -> Path:
        """Returns root of project"""
        dot_project_files = [x for x in files if ".project" == Path(x).name]
        dot_classpath_files = [x for x in files if ".classpath" == Path(x).name]
        pom_files = [x for x in files if "pom.xml" == Path(x).name]

        # One of each file and correct type
        error = ""
        if len(dot_project_files) != 1:
            error += f"Expected 1 .project file but found {len(dot_project_files)}\n"
        if len(dot_classpath_files) != 1:
            error += (
                f"Expected 1 .classpath file but found {len(dot_classpath_files)}\n"
            )
        if len(pom_files) < 1:
            error += f"Expected 1 pom.xml file but found 0\n"

        if error:
            raise ProjectValidationException(error)

        dot_project = Path(dot_project_files[0])
        dot_classpath = Path(dot_classpath_files[0])
        pom = Path(pom_files[0])

        if dirname(dot_project) != dirname(dot_classpath) or dirname(
            dot_project
        ) != dirname(pom):
            raise Exception("Config files are not all at same level")
        return Path(dirname(dot_project))

    def get_project_root(self, directory_root: Path) -> Path:
        """
        Raises ProjectInstallException if is not a project

        :return: Project root or None if there is no enclosing directory
        """
        namelist: list[str] = []
        for x in directory_root.walk():
            path, dirs, files = x
            for dir in dirs:
                namelist.append((path / dir).as_posix() + "/")
            for file in files:
                namelist.append((path / file).as_posix())
        return self.__is_project(namelist)
