from typing import Literal, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET 
from xml.etree.ElementTree import Element
from ..project_validation_exception import ProjectValidationException

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
    def __init__(self, classpath_file: Path, classpath_entries: list[ClasspathEntry]):
        self.classpath_entries = classpath_entries
    
    @classmethod
    def create(cls, classpath_file: Path) -> 'DotClasspath':
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
                        raise ProjectValidationException(f'\'name\' attribute expected but not found on attribute field in {classpath_file}')
                    if not value:
                        raise ProjectValidationException(f'\'value\' attribute expected but not found on attribute field in {classpath_file}')
                    attributes[name] = value
            entry_dict['attributes'] = attributes

            classpath_entries.append(ClasspathEntry(**entry_dict)) # type: ignore
        return DotClasspath(classpath_file, classpath_entries)
    
    def classpath(self) -> list[str]:
        ...