from os.path import dirname
from pathlib import Path
from zipfile import ZipFile

from Atypes import Submission


class MavenProjectValidator:

    @classmethod
    def validate_and_extract_zipfile(cls, submission: Submission, zipfile: ZipFile, workspace: Path) -> Path:
        # Returns extracted files name or raises RuntimeException
        project_root: Path = cls.__find_maven_project_root_from_files(zipfile.namelist())

        if project_root is None:
            raise NotImplementedError(".project is zipped without a root directory")
        elif len(project_root.parts) == 1:
            zipfile.extractall(workspace)
        else:
            raise NotImplementedError(f".project is deeply nested in zip file located at {project_root}")

        extracted_file = workspace / project_root
        # Validate naming
        for name in submission.student.name_tokens:
            if name in extracted_file.name:
                break
        else:
            print(
                f"{submission.student.name} improperly named their project directory as {extracted_file.name}"
            )

        # Rename
        new_extracted_file = Path(workspace) / submission.get_filename()

        if new_extracted_file.exists():
            new_extracted_file.unlink()
        extracted_file.rename(new_extracted_file)

        return new_extracted_file


    @classmethod
    def __find_maven_project_root_from_files(cls, files: list[str]) -> Path:
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
            raise RuntimeError(error)

        dot_project = Path(dot_project_files[0])
        dot_classpath = Path(dot_classpath_files[0])
        pom = Path(pom_files[0])

        if dirname(dot_project) != dirname(dot_classpath) or dirname(
            dot_project
        ) != dirname(pom):
            raise Exception("Config files are not all at same level")
        return Path(dirname(dot_project))
