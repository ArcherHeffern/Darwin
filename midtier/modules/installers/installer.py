from models.backend_models import Student, FileSubmission, FileSubmissionGroup
from typing import Optional
from zipfile import is_zipfile, ZipFile
from clients.client_I import Client_I
from clients.student_filterer import StudentFilterer
from utils import Logger
from os import makedirs, remove
from pathlib import Path

from validators_and_executors.project_validator_I import ProjectValidator_I


class Installer:
    def __init__(
        self,
        client: Client_I,
        validator: ProjectValidator_I,
        logger: Logger,
        workspace: str = ".",
    ):
        self.client = client
        self.validator = validator
        self.logger = logger
        self.workspace = workspace
        makedirs(self.workspace, exist_ok=True)

    class FileManager:
        def __init__(self, file: Path):
            self.file = file

        def __enter__(self): ...

        def __exit__(self, *args):
            remove(self.file)

    def get_students(self, student_filterer: StudentFilterer) -> list[Student]:
        return self.client.get_students(student_filterer)

    def install_student_submission(
        self,
        student: Student,
        file_submission: FileSubmission,
        file_submission_group: FileSubmissionGroup,
    ) -> Optional[Path]:
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
        assert (
            not file_submission_group.grading_data.graded
        ), "File Submission Group has already been graded"

        l = self.logger

        zip_file_path = Path(self.workspace) / (
            file_submission_group.get_filename(student) + ".zip"
        )

        self.client.install_file(file_submission.download_url, zip_file_path)

        with self.FileManager(
            zip_file_path
        ):  # Deletes zipfile when leaving function scope
            l.log("=============")
            if is_zipfile(zip_file_path):
                with ZipFile(zip_file_path, "r") as zip_ref:
                    l.log(f"{student.name} zipfile")

                    project_root: Path = self.validator.get_zip_project_root(
                        zip_ref.namelist()
                    )

                    if project_root is None:
                        raise NotImplementedError(
                            ".project is zipped without a root directory"
                        )
                    elif len(project_root.parts) == 1:
                        zip_ref.extractall(self.workspace)
                    else:
                        raise NotImplementedError(
                            f".project is deeply nested in zip file located at {project_root}"
                        )
            else:
                raise NotImplementedError("no zipfile!")
            file = self.__validate_extracted_file(
                student, file_submission_group, project_root
            )

            file_submission.file = file

            return file

    def __validate_extracted_file(
        self,
        student: Student,
        file_submission_group: FileSubmissionGroup,
        extracted_file: Path,
    ) -> Path:
        """
        Renames extracted file and sets flags on student if improperly named

        :param extracted_file: Path of extracted file not including workspace section
        """
        # Validate naming
        for name in student.name_tokens:
            if name in extracted_file.name:
                break
        else:
            self.logger.error(
                f"{student.name} improperly named their project directory as {extracted_file.name}"
            )
            file_submission_group.grading_data.proper_naming = False

        # Rename anyways
        extracted_file = Path(self.workspace) / extracted_file
        new_extracted_file = Path(self.workspace) / Path(
            file_submission_group.get_filename(student)
        )
        if not new_extracted_file.exists():
            extracted_file.rename(new_extracted_file)

        return new_extracted_file
