from os import chdir, getcwd
from subprocess import run
from Atypes import (
    Assignment,
	TestResult,
)
from moodle_client import MoodleClient
from student_filterer import StudentFilterer
from installer import Installer
from store_grade_to_file import StoreGradesToFile
from maven_project import MavenProject
from maven_project_validator import (
    MavenProjectValidator,
)
from traceback import format_exception
import dotenv
from pprint import PrettyPrinter
from sys import stderr
from pathlib import Path

# ======== PA Context ========
PA_NAME = "3"
SKELETON: Path = Path("pa3")
prev_dir = getcwd()
chdir(SKELETON)
run(["mvn", "compile"])
chdir(prev_dir)
exit()
TESTS_TO_RUN: list[str] = ["BehaviorTest", "SimulationTest"]
TEST_OUTPUT_FILE_NAMES = ["TEST-cs131.pa3.BehaviorTest.xml", "TEST-cs131.pa3.SimulationTest.xml"]
student_filterer = StudentFilterer().filter_last_name("cohen", "cohen")

# ======== Arguments ========
INSTALL_ONLY = False
SAFE_MODE = (
    False  # Does not install anything - Instead prints students specified by your range
)
TEST_REPORT_LOCATIONS = [Path(f"./target/surefire-reports/{TEST_OUTPUT_FILE_NAME}") for TEST_OUTPUT_FILE_NAME in TEST_OUTPUT_FILE_NAMES]

# ========= Constants =========
TEST_CLASSES_LOCATION = Path("./target/test-classes")
WORKSPACE_DIR = Path("./workspace")
OUTFILE: Path = Path("out.txt")

env = dotenv.dotenv_values()
pprint = PrettyPrinter().pprint
assignment = Assignment(PA_NAME)

def grade():
    moodle_session = env.get("MOODLE_SESSION")
    assignment_id = env.get("ASSIGNMENT_ID")
    if not moodle_session:
        print("MOODLE_SESSION not found in .env", file=stderr)
        exit(1)
    if not assignment_id:
        print("ID not found in .env", file=stderr)
        exit(1)

    # Installation Services
    moodle_client = MoodleClient(moodle_session, assignment_id)
    maven_project_validator = MavenProjectValidator()
    installer = Installer(moodle_client, maven_project_validator, WORKSPACE_DIR)

    # ======== Runtime Errors ========
    ERRORS: list[str] = []

    with StoreGradesToFile(assignment, OUTFILE) as storage_service:

        students = moodle_client.get_students()
        students = student_filterer.filter(students)
        if SAFE_MODE:
            print("======== Students ========")
            pprint(students)
            exit(0)
        for student in students:
            print(f"{student.name}=============")
            if len(student.submissions) == 0:
                error_msg = f"{student.name} has no submissions..."
                print(error_msg)
                ERRORS.append(error_msg)
            if len(student.submissions) > 1:
                error_msg = f"Student '{student.name}' has more than 1 submission"
                print(error_msg)
                ERRORS.append(error_msg)

            for submission in student.submissions:
                # ==== Installation and Validation ====
                try:
                    project_root: Path = installer.install_submission(submission)
                except Exception as e:
                    error_msg = f"Issue with installing '{student.name}' submission: {e}"
                    print(error_msg)
                    ERRORS.append(error_msg)
                    continue

                if INSTALL_ONLY:
                    continue

                # ==== Test Running ====
                project = MavenProject(project_root, SKELETON, TEST_CLASSES_LOCATION, TESTS_TO_RUN, TEST_REPORT_LOCATIONS, 60)
                try:
                    results: list[TestResult] = project.test(project_root)
                except Exception as e:
                    error_msg = f"Issue with running '{student.name}' tests: {''.join(format_exception(e))}"
                    print(error_msg)
                    ERRORS.append(error_msg)
                    continue

                # ======== Grading =======
                try:
                    storage_service.store_grade(student, results)
                except Exception as e:
                    print(f"Issue with uploading grades '{student.name}' because of {e}")
