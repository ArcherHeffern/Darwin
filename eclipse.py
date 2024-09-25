from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from abc import abstractmethod, ABC
from typing import Literal, Optional, TypeAlias, NewType, Any
from os import PathLike
import xml.etree.ElementTree as ET 
from xml.etree.ElementTree import Element

class StrAble:
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        if not hasattr(self, '_fields'):
            self._fields = [d for d in dir(self) if not d.startswith('_') and not callable(getattr(self, d)) and d.upper() != d]
        f = {k: getattr(self, k) for k in self._fields}
        return f'<{self.__class__.__name__}, {str(f)}>'

class ICommand(StrAble):
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
    
class DotProject(IProjectDescription, StrAble):
    """
    eclipse projects are defined using the .project file

    specification: https://help.eclipse.org/latest/index.jsp?topic=%2Forg.eclipse.platform.doc.isv%2Freference%2Fmisc%2Fproject_description_file.html&cp=2_1_5_11
    """

    def __init__(self, name: Optional[str], comment: Optional[str], projects: list[IProject], buildspec: list[ICommand], natures: list[str], linkedResources: list, project_root: Path):
        """
        :param projects list[IProject]:
        :param buildspec list[ICommand]: # TODO: Complete argument parsing
        :param natures list[str]:
        list[IProject]
        :param linkedResources list: # TODO
        """
        self.name = name
        self.comment = comment
        self.projects: list[IProject] = projects
        self.buildspec: list[ICommand] = buildspec
        self.natures: list[str] = natures
        self.linkedResources: list[IProject] = linkedResources
        self.root_folder: Path = project_root

    @classmethod
    def create(cls, project_root: Path):
        element_tree = ET.parse(project_root)
        name: str = element_tree.find('name').text # type: ignore
        comment: Optional[str] = element_tree.find('comment').text # type: ignore
        build_commands: list[ICommand] = []
        buildspec_node: Element = element_tree.find('buildSpec') # type: ignore
        for build_command_node in buildspec_node:
            command_name = getattr(build_command_node.find('name'), 'text')
            # TODO: Handle arguments
            build_commands.append(ICommand(command_name, []))

        natures: list[str] = []
        nature_nodes = element_tree.find('natures')
        if nature_nodes is not None:
            for nature_node in nature_nodes:
                if nature_node.text:
                    natures.append(nature_node.text)
        return cls(name, comment, [], build_commands, natures, [], project_root)

    def getBuildSpec(self) -> list[ICommand]:
        """Returns the list of build commands to run when building the described project."""
        return self.buildspec

    def getComment(self) -> str:
        """Returns the descriptive comment for the described project."""
        return self.comment or ''

    def getLocation(self) -> str:
        """Returns the local file system location for the described project."""
        raise NotImplementedError

    def getName(self) -> str:
        """Returns the name of the described project."""
        return self.name or ''
    
    def getNatureIds(self) -> list[str]:
        """Returns the list of natures associated with the described project."""
        return self.natures

    def getReferencedProjects(self) -> list[IProject]:
        """Returns the projects referenced by the described project."""
        raise NotImplementedError

    def hasNature(self, natureId: str) -> bool:
        """Returns whether the project nature specified by the given nature extension id has been added to the described project."""
        return natureId in self.natures

    def newCommand(self) -> ICommand:
        """Returns a new build command."""
        raise NotImplementedError

    def setBuildSpec(self, buildspec: list[ICommand]):
        """Sets the list of build command to run when building the described project."""
        raise NotImplementedError

    def setComment(self, comment: str):
        """Sets the comment for the described project."""
        raise NotImplementedError

    def setLocation(self, location: PathLike):
        """Sets the local file system location for the described project."""
        raise NotImplementedError

    def setName(self, projectName: str):
        """Sets the name of the described project."""
        raise NotImplementedError

    def setNatureIds(self, natures: list[str]):
        """Sets the list of natures associated with the described project."""
        raise NotImplementedError

    def setReferencedProjects(self, projects: list[IProject]):
        """Sets the referenced projects, ignoring any duplicates."""
        raise NotImplementedError

@dataclass
class ClasspathEntry:
    kind: Literal['src', 'output', 'con']
    attributes: dict[str, str]
    path: Optional[str]
    output: Optional[str] = None
    
class DotClasspath:
    """
    .classpath file parser
    
    (Kind of) file format: https://eclim.org/vim/java/classpath.html
    """
    def __init__(self, classpath_entries: list[ClasspathEntry]):
        self.classpath_entries = classpath_entries
    
    class ParseClasspathException(RuntimeError):
        """Could not parse classpath"""

    @classmethod
    def create(cls, classpath_file: Path) -> Optional['DotClasspath']:
        """
        Parses eclipse .classpath file

        Warning! Poor error handling since I could not find an actual specification. Quite a few bugs are bound to show up.
        """
        element_tree = ET.parse(classpath_file)
        classpath_entry_nodes = element_tree.findall('classpathentry')

        classpath_entries: list[ClasspathEntry] = []
        for classpath_entry in classpath_entry_nodes:
            entry_dict: dict[Any, Any] = dict(classpath_entry.items())
            attributes = {}
            attributes_node = classpath_entry.find('attributes')
            if attributes_node is not None:
                for attribute_node in attributes_node:
                    name = attribute_node.get('name')
                    value = attribute_node.get('value')
                    if not name:
                        raise cls.ParseClasspathException(f'\'name\' attribute expected but not found on attribute field in {classpath_file}')
                    if not value:
                        raise cls.ParseClasspathException(f'\'value\' attribute expected but not found on attribute field in {classpath_file}')
                    attributes[name] = value
            entry_dict['attributes'] = attributes

            classpath_entries.append(ClasspathEntry(**entry_dict)) # type: ignore
        pprint(classpath_entries)
        return DotClasspath(classpath_entries)
    
    def classpath(self) -> list[str]:
        ...


class DotSettings:
    ...


class Pom:
    ...


class Eclipse:

    BuildSystem: TypeAlias = Literal['eclipse', 'maven', 'gradle']

    def __init__(self, project_root: Path, build_system: BuildSystem):
        self.project_root = project_root
        self.build_system = build_system

    @classmethod
    def create(cls, project_root: Path) -> Optional['Eclipse']:
        _build_system: Literal['eclipse', 'maven', 'gradle']
        _class_path: list[str]
        _compile_commands: list[str]
    
    def build(self):
        ...
    
    def run_tests(self):
        ...
