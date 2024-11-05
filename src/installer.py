from maven_project_validator import MavenProjectValidator
from Atypes import Submission
from zipfile import is_zipfile, ZipFile
from os import makedirs, remove
from pathlib import Path
from moodle_client import MoodleClient


class Installer:
    def __init__(
        self,
        client: MoodleClient,
        validator: MavenProjectValidator,
        workspace: Path = Path("."),
    ):
        self.validator = validator
        self.client = client
        self.workspace = workspace
        makedirs(self.workspace, exist_ok=True)

    def install_submission(
        self,
        submission: Submission
    ) -> Path:
        """
        Completes all operations for installing and validating a java project.

        Zip file is deleted when leaving this scope

        :param student Student:
        :param file_submission FileSubmission:

        - Installs folder
        - Extracts if zipfile
        - Deletes zipfile if exists
        - Returns java project file if is a project
        - Deletes folder is is not
        """

        temporary_install_path = Path(self.workspace) / ("temp_" + submission.get_filename())

        self.client.download_file(submission.download_url, temporary_install_path)

        with self.FileManager(temporary_install_path):  
            if is_zipfile(temporary_install_path):
                with ZipFile(temporary_install_path, "r") as zip_ref:
                    self.validator.validate_and_extract_zipfile(submission, zip_ref, self.workspace)
            else:
                raise NotImplementedError("no zipfile!")

            submission.file = Path(Path(self.workspace) / submission.get_filename())
        return submission.file


    class FileManager:
        def __init__(self, file: Path):
            self.file = file

        def __enter__(self): ...

        def __exit__(self, *args):
            remove(self.file)