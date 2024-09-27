from typing import Optional
from pathlib import Path
from .project_description_I import IProjectDescription, ICommand, IProject
import xml.etree.ElementTree as ET 
from os import PathLike

class DotProject(IProjectDescription):
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
    def create(cls, dot_project: Path):
        element_tree = ET.parse(dot_project)
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
        return cls(name, comment, [], build_commands, natures, [], dot_project)

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