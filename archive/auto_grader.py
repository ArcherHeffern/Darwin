from models.backend_models import (
    Assignment,
    AssignmentMetadata,
    Student,
    FileSubmissionGroup,
    FileSubmission,
    GradingData,
)
from clients.moodle.moodle_client import MoodleClient
from clients.student_filterer import StudentFilterer
from midtier.modules.installers.installer import Installer
from storage.csv_storage import CSVStorage
from validators_and_executors.eclipsemaven.project_impl import MavenProject
from validators_and_executors.eclipsemaven.project_validator_Impl import (
    MavenProjectValidator,
)
from traceback import format_exception
from datetime import datetime
import dotenv
from pprint import PrettyPrinter
from midtier.utils import Logger
from sys import stderr
from pathlib import Path
from typing import Optional, Literal

# ======== PA Context ========

PA_NAME = "1"
DUE_DATE = datetime(2024, 9, 19, 23, 59, 59)
# DATE_TO_RUN =
# FREQUENCY_OF_RERUNS: literal['exponential-backoff', 'linear']
# MAX_RERUNS: int = 3
SOURCE: Literal["moodle"] = "moodle"
PROJECT_TYPE: Literal["maven"] = "maven"
TEST_CLASS_FILES: Path = Path("./compiled_testfiles").absolute()
TESTS_TO_RUN: list[str] = ["AllSequentialTests"]

METADATA = AssignmentMetadata(None)

# ======== Assignment Config ========
assignment = Assignment(
    None, PA_NAME, DUE_DATE, SOURCE, PROJECT_TYPE, TESTS_TO_RUN, METADATA
)

# ======== Arguments ========
WORKSPACE_DIR = "./workspace"
# WORKSPACE_DIR = '/Users/archerheffern/fall2024OS_pa1/'
PRINT_ALL_STUDENTS = False  # Prints all students scraped from html
SAFE_MODE = (
    False  # Does not install anything - Instead prints students specified by your range
)
VERBOSE_DOWNLOAD: bool = True
VERBOSE_PROJECT_VALIDATION: bool = True
VERBOSE_TEST_RUNNING: bool = True
VERBOSE_GRADING: bool = True
VERBOSE_GRADE_UPLOADING: bool = True
OUTFILE: Path = Path("out.csv")

# ======== Runtime Errors ========
DOWNLOAD_ERRORS: list[
    tuple["Student", "FileSubmissionGroup", "FileSubmission", Exception]
] = []
VALIDATION_ERRORS: list[
    tuple["Student", "FileSubmissionGroup", "FileSubmission", Exception]
] = []
TEST_RUNNER_ERRORS: list[
    tuple["Student", "FileSubmissionGroup", "FileSubmission", Exception]
] = []

env = dotenv.dotenv_values()
pprint = PrettyPrinter().pprint


if __name__ == "__main__":
    # Setup

    moodle_session = env.get("MOODLE_SESSION")
    _id = env.get("ID")
    if not moodle_session:
        print("MOODLE_SESSION not found in .env", file=stderr)
        exit(1)
    if not _id:
        print("ID not found in .env", file=stderr)
        exit(1)

    # Installation Services
    moodle_client = MoodleClient(moodle_session, _id, assignment)
    install_logger = Logger(VERBOSE_DOWNLOAD, "INSTALL")
    installer = Installer(
        moodle_client, MavenProjectValidator(), install_logger, WORKSPACE_DIR
    )
    student_filterer = StudentFilterer()

    # Project Validation Services
    project_validation_logger = Logger(VERBOSE_PROJECT_VALIDATION, "PROJECT VALIDATION")
    project_validator = MavenProjectValidator()
    project = MavenProject(
        TEST_CLASS_FILES,
        Path("./target/test-classes"),
        TESTS_TO_RUN,
        Path("./target/surefire-reports/TEST-cs131.pa1.AllSequentialTests.xml"),
        2.5,
    )

    # Test Running Services
    test_running_logger = Logger(VERBOSE_TEST_RUNNING, "TEST RUNNER")

    # Grading Services
    grading_logger = Logger(VERBOSE_GRADING, "GRADER")

    # Grade Uploading Services
    grade_upload_logger = Logger(VERBOSE_GRADE_UPLOADING, "GRADE UPLOADER")
    with CSVStorage(assignment, OUTFILE) as storage_service:

        students = installer.get_students(student_filterer)

        if PRINT_ALL_STUDENTS:
            print("======== All Students ========")
            pprint(students)
        students = student_filterer.filter(students)
        if SAFE_MODE:
            print("======== Filtered Students ========")
            pprint(students)
            exit(0)
        for student in students:
            if len(student.submissions) == 0:
                print("=============")
                print(f"{student.account.name} has no submissions...")
            if len(student.submissions) > 1:
                print("NOT IMPLEMENTED HANDLING Student has more than 1 submission")
                student.submissions = [student.submissions[0]]

            for submission in student.submissions:
                for file_submission in submission.file_submissions:
                    # ==== Installation and Validation ====
                    try:
                        maybe_project_root: Optional[Path] = (
                            installer.install_student_submission(
                                student, file_submission, submission
                            )
                        )
                        if not maybe_project_root:
                            continue
                    except Exception as e:
                        install_logger.error(
                            f"Issue with installing '{student.account.name}' submission: {e}"
                        )
                        DOWNLOAD_ERRORS.append(
                            (student, submission, file_submission, e)
                        )
                        continue

                    project_root = maybe_project_root

                    # ==== Test Running ====
                    try:
                        results = project.run(project_root)
                    except Exception as e:
                        test_running_logger.error(
                            f"Issue with running '{student.account.name}' tests: {''.join(format_exception(e))}"
                        )
                        TEST_RUNNER_ERRORS.append(
                            (student, submission, file_submission, e)
                        )
                        continue

                    # ======== Grading ========
                    try:
                        ...
                    except Exception as e:
                        grading_logger.error(
                            f"Issue with grading '{student.name}' because of {e}"
                        )

                    try:
                        storage_service.upload_grade(student, results)
                    except Exception as e:
                        grade_upload_logger.error(
                            f"Issue with uploading grades '{student.name}' because of {e}"
                        )
