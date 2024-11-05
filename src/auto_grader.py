from os import chdir, getcwd
from subprocess import DEVNULL, run
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
from pprint import pprint
from sys import stderr
from pathlib import Path

# ======== PA Context ========
PA_NAME = "3"
SKELETON: Path = Path("pa3").absolute()
TESTS_TO_RUN: list[str] = ["BehaviorTest", "SimulationTest"]
TEST_OUTPUT_FILE_NAMES = ["TEST-cs131.pa3.BehaviorTest.xml", "TEST-cs131.pa3.SimulationTest.xml"]
student_filterer = StudentFilterer()

# ======== Arguments ========
INSTALL_ONLY = False
SAFE_MODE = (
    False  # Does not install anything - Instead prints students specified by your range
)
TEST_REPORT_LOCATIONS = [Path(f"./target/surefire-reports/{TEST_OUTPUT_FILE_NAME}") for TEST_OUTPUT_FILE_NAME in TEST_OUTPUT_FILE_NAMES]

# ========= Constants =========
TEST_CLASSES_LOCATION = Path("./target/test-classes")
WORKSPACE_DIR = Path("./workspace").absolute()
OUTFILE: Path = Path("out.txt")

if __name__ == '__main__':
    env = dotenv.dotenv_values()
    moodle_session = env.get("MOODLE_SESSION")
    assignment_id = env.get("ASSIGNMENT_ID")
    if not moodle_session:
        print("MOODLE_SESSION not found in .env", file=stderr)
        exit(1)
    if not assignment_id:
        print("ASSIGNMENT_ID not found in .env", file=stderr)
        exit(1)

    # Installation Services
    ASSIGNMENT = Assignment(assignment_id, PA_NAME)
    moodle_client = MoodleClient(moodle_session, ASSIGNMENT)
    maven_project_validator = MavenProjectValidator()
    installer = Installer(moodle_client, maven_project_validator, WORKSPACE_DIR)
    ERRORS: list[str] = []

    # Setup
    print("Compiling test-classes")
    prev_dir = getcwd()
    chdir(SKELETON)
    run(["mvn", "clean"], stdout=DEVNULL)
    run(["mvn", "test-compile"], stdout=DEVNULL)
    chdir(prev_dir)

    with StoreGradesToFile(ASSIGNMENT, OUTFILE) as storage_service:
        print("Getting students from moodle")
        students = moodle_client.get_students()
        students = student_filterer.filter(students)
        if SAFE_MODE:
            print("======== Students ========")
            pprint(students)
            exit(0)

        print("Grading Submissions")
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
                project = MavenProject(project_root.absolute(), SKELETON, TEST_CLASSES_LOCATION, TESTS_TO_RUN, TEST_REPORT_LOCATIONS, 60)
                try:
                    results: list[TestResult] = project.test(project_root)
                except Exception as e:
                    error_msg = f"Issue with running '{student.name}' tests: {''.join(format_exception(e))}"
                    print(error_msg)
                    ERRORS.append(error_msg)
                    continue

                # ======== Grading =======
                try:
                    storage_service.store_grade(student, results, TESTS_TO_RUN)
                except Exception as e:
                    print(f"Issue with uploading grades '{student.name}' because of {e}")
