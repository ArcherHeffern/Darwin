from abc import ABC, abstractmethod
from os import PathLike
from typing import NewType

class ICommand:
    def __init__(self, command: str, args: list[str]):
        self.command = command
        self.args = args

    def __str__(self):
        ...

IProject = NewType('IProject', str)

class IProjectDescription(ABC):
    """Interface Specification: https://archive.eclipse.org/eclipse/downloads/documentation/2.0/html/plugins/org.eclipse.platform.doc.isv/reference/api/org/eclipse/core/resources/IProjectDescription.html"""

    DESCRIPTION_FILE_NAME: str = '.project'
    NATURES = {
		'org.eclipse.jdt.core.javanature': 'java', 
		'org.eclipse.buildship.core.gradleprojectnature': 'gradle', 
		'org.eclipse.m2e.core.maven2Nature': 'maven', 
		'org.eclipse.pde.core.org.eclipse.pde.PluginNature': 'plugin', 
		'org.eclipse.pde.core.org.eclipse.pde.FeatureNature': 'feature', 
		'org.eclipse.pde.core.org.eclipse.pde.UpdateSiteNature': 'updatesite', 
    }

    @abstractmethod
    def getBuildSpec() -> list[ICommand]:
        """Returns the list of build commands to run when building the described project."""
        raise NotImplementedError

    @abstractmethod
    def getComment() -> str:
        """Returns the descriptive comment for the described project."""
        raise NotImplementedError

    @abstractmethod
    def getLocation() -> str:
        """Returns the local file system location for the described project."""
        raise NotImplementedError

    @abstractmethod
    def getName() -> str:
        """Returns the name of the described project."""
        raise NotImplementedError
    
    @abstractmethod
    def getNatureIds() -> list[str]:
        """Returns the list of natures associated with the described project."""
        raise NotImplementedError

    @abstractmethod
    def getReferencedProjects() -> list[IProject]:
        """Returns the projects referenced by the described project."""
        raise NotImplementedError

    @abstractmethod
    def hasNature(self, natureId: str) -> bool:
        """Returns whether the project nature specified by the given nature extension id has been added to the described project."""
        raise NotImplementedError

    @abstractmethod
    def newCommand() -> ICommand:
        """Returns a new build command."""
        raise NotImplementedError

    @abstractmethod
    def setBuildSpec(self, buildspec: list[ICommand]):
        """Sets the list of build command to run when building the described project."""
        raise NotImplementedError

    @abstractmethod
    def setComment(self, comment: str):
        """Sets the comment for the described project."""
        raise NotImplementedError

    @abstractmethod
    def setLocation(self, location: PathLike):
        """Sets the local file system location for the described project."""
        raise NotImplementedError

    @abstractmethod
    def setName(self, projectName: str):
        """Sets the name of the described project."""
        raise NotImplementedError

    @abstractmethod
    def setNatureIds(self, natures: list[str]):
        """Sets the list of natures associated with the described project."""
        raise NotImplementedError

    @abstractmethod
    def setReferencedProjects(self, projects: list[IProject]):
        """Sets the referenced projects, ignoring any duplicates."""
        raise NotImplementedError