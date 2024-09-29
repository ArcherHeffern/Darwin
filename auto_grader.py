import requests
from validators_and_executors.eclipsemaven.project_impl import MavenProject
from validators_and_executors.project_validator_I import ProjectValidator_I
from validators_and_executors.eclipsemaven.project_validator_Impl import MavenProjectValidator
from traceback import format_exception
from colorama import Style, Fore
from calendar import Month
from itertools import chain
from collections import defaultdict
from datetime import datetime, timedelta
import dotenv
from pprint import PrettyPrinter
from zipfile import ZipFile, is_zipfile
from os import remove, makedirs, path
from sys import stderr
from pathlib import Path
from regex import Match, match
from bs4 import BeautifulSoup
from typing import Optional, Self
from dataclasses import dataclass, field

# ======== PA Context ========

PA_NUMBER = 1
DUE_DATE = datetime(2024, 9, 19, 23, 59, 59)

# ======== Arguments ========
WORKSPACE_DIR = './workspace'
# WORKSPACE_DIR = '/Users/archerheffern/fall2024OS_pa1/'
SAVE_HTML: Optional[str] = None
PRINT_ALL_STUDENTS = False # Prints all students scraped from html
SAFE_MODE = False # Does not install anything - Instead prints students specified by your range
INPUT_FILE: Optional[str] = 'out.html'
VERBOSE_DOWNLOAD: bool = True 
VERBOSE_PROJECT_VALIDATION: bool = True 
VERBOSE_TEST_RUNNING: bool = True

# ======== Runtime Errors ========
DOWNLOAD_ERRORS: list[tuple['Student', 'FileSubmissionGroup', 'FileSubmission', Exception]] = []
VALIDATION_ERRORS: list[tuple['Student', 'FileSubmissionGroup', 'FileSubmission', Exception]] = []
TEST_RUNNER_ERRORS: list[tuple['Student', 'FileSubmissionGroup', 'FileSubmission', Exception]] = []

env = dotenv.dotenv_values()
pprint = PrettyPrinter().pprint

class Logger:
    def __init__(self, enabled: bool = True, name: str = ''):
        self.enabled = enabled
        if name:
            name = '[' + name + '] '
        self.name: str = name
    
    def log(self, s: str):
        if self.enabled:
            print(self.name + s)
    
    def error(self, s: str):
        if self.enabled:
            print(f"{Fore.RED}{self.name}{s}{Style.RESET_ALL}", file=stderr)

@dataclass
class FileSubmission:
    download_url: str
    date: datetime
    file: Optional[Path] = None


@dataclass
class GradingData:
    # Assume positive unless proven otherwise
    late: Optional[timedelta] = None
    proper_naming: bool = True
    grade: Optional[int] = None

    @property
    def graded(self):
        return self.grade is not None

class FileSubmissionGroup:
    def __init__(self, file_submissions: list[FileSubmission]):
        assert len(file_submissions) > 0

        self.file_submissions = file_submissions

        # All submissions in FileSubmissionGroup must have the same date
        self.date: datetime = file_submissions[0].date 

        lateness = None
        if self.date > DUE_DATE:
            lateness = self.date - DUE_DATE
        self.grading_data: GradingData = GradingData(late=lateness)
        self.__filename: Optional[str] = None
    
    def __str__(self) -> str:
        return str(self.file_submissions)

    def __repr__(self) -> str:
        return str(self.file_submissions)

    @property
    def late(self) -> bool:
        return DUE_DATE < self.date
    
    def get_filename(self, student: 'Student') -> str:
        if self.__filename:
            return self.__filename
        filename: str = str(student.sid) + "_" + "".join(student.name_tokens) + "_PA" + str(PA_NUMBER)
        self.__filename = filename
        return filename

@dataclass
class Student:
    sid: int # Student id
    name: str # Capitalized
    name_tokens: list[str] # Each capitalized
    email: str
    submissions: list[FileSubmissionGroup] = field(default_factory=list)

def flatmap(func, *iterable):
    return chain.from_iterable(map(func, *iterable))

class MoodleClient:

    url = 'https://moodle.brandeis.edu/mod/assign/view.php'


    headers = {
        'Accept': 'text/html',
        'Host': 'moodle.brandeis.edu',
    }


    def __init__(self, moodle_session: str, id: str):
        self.cookies = {
            'MoodleSession': moodle_session,
        }

        self.params = {
        'id': id,
        'tifirst': '',
        'tilast': '',
        'action': 'grading'
        }

    def get_html(self) -> str:
        r = requests.get(
            url=self.url,
            params=self.params,
            headers=self.headers,
            cookies=self.cookies
        )

        assert r.status_code == 200

        return r.text
    
    def install_file(self, url: str, destination: Path):
        response = requests.get(
            url=url,
            headers=self.headers,
            cookies=self.cookies
        )
        assert response.status_code == 200

        with open(destination, 'wb') as f:
            f.write(response.content)


class StudentParser:

    def parse_html(self, html: str) -> list[Student]:
        soup = BeautifulSoup(html, features='lxml')
        submissions = soup.find_all('tr')
        submissions = filter(self.__check_if_submission, submissions)

        students: list[Student] = []

        for submission in submissions:
            sid: int
            name: str
            email: str
            file_submissions: list[FileSubmissionGroup]

            sid = submission['class'][0].removeprefix('user')
            name_tokens = [t.capitalize() for t in submission.findChild("td", class_='cell c2').text.split()]
            name = " ".join(name_tokens)
            email = submission.findChild("td", class_='cell c3 email').text.strip()
            submitted = self.__has_submission(submission)

            if submitted:
                file_submissions = self.__parse_submissions(submission)
            else:
                file_submissions = []
            
            students.append(Student(sid, name, name_tokens, email, file_submissions))
        return students
            
    def __parse_submissions(self, submission) -> list[FileSubmissionGroup]:
        submission = submission.findChild("td", class_='cell c9')
        file_submission_nodes = submission.findChildren('div', class_='fileuploadsubmission') 
        file_submission_time_nodes = submission.findChildren('div', class_='fileuploadsubmissiontime')

        time_groups: defaultdict[datetime, list[FileSubmission]] = defaultdict(list)
        for file_submission_node, file_submission_time_node in zip(file_submission_nodes, file_submission_time_nodes):
            submission_url: str = file_submission_node.find('a')['href']
            submission_time: datetime = self.__parse_submission_time(file_submission_time_node.text.strip())
            time_groups[submission_time].append(FileSubmission(submission_url, submission_time))

        file_submission_groups: list[FileSubmissionGroup] = []
        for group_of_file_submissions in time_groups.values():
            file_submission_groups.append(FileSubmissionGroup(group_of_file_submissions))

        return file_submission_groups

    def __parse_submission_time(self, s: str) -> datetime:
        """September 19 2024, 4:11 PM"""
        tokens: list[str] = list(flatmap(lambda s: s.split(":"), flatmap(str.split, s.split(",")))) # type: ignore
        month: int = Month[tokens[0].upper()]
        day: int = int(tokens[1])
        year: int = int(tokens[2])
        hour: int = int(tokens[3])
        minute: int = int(tokens[4])
        period: str = tokens[5]
        if period == 'AM':
            ...
        elif period == 'PM':
            if hour != 12:
                hour += 12
        else:
            raise ValueError(f'Expected AM or PM but found {period}')
        return datetime(year, month, day, hour, minute)

    def __check_if_submission(self, submission):
        if not submission.get('class'):
            return False
        return match("user\\d+", submission['class'][0])
    
    def __has_submission(self, submission) -> bool:
        return bool(submission.findChild("td", class_='cell c4').findChild('div', class_='submissionstatussubmitted'))
    
class Installer:
    def __init__(self, moodle_client: MoodleClient, logger: Logger, workspace: str = '.'):
        self.moodle_client = moodle_client
        self.logger = logger
        self.workspace = workspace
        makedirs(self.workspace, exist_ok=True)
    
    class FileManager:
        def __init__(self, file: Path):
            self.file = file
        
        def __enter__(self):
            ...
        
        def __exit__(self, *args):
            remove(self.file)
    
    def install(self, student: Student, file_submission: FileSubmission, file_submission_group: FileSubmissionGroup, validator: ProjectValidator_I) -> Optional[Path]:
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
        assert not file_submission_group.grading_data.graded, 'File Submission Group has already been graded'

        l = self.logger

        zip_file_path = Path(self.workspace) / (file_submission_group.get_filename(student) + ".zip")

        self.moodle_client.install_file(file_submission.download_url, zip_file_path)

        with self.FileManager(zip_file_path): # Deletes zipfile when leaving function scope
            l.log('=============')
            if is_zipfile(zip_file_path):
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    l.log(f'{student.name} zipfile')

                    project_root: Path = validator.get_zip_project_root(zip_ref.namelist())

                    if project_root is None:
                        raise NotImplementedError('.project is zipped without a root directory')
                    elif len(project_root.parts) == 1:
                        zip_ref.extractall(self.workspace)
                    else:
                        raise NotImplementedError(f'.project is deeply nested in zip file located at {project_root}')
            else:
                raise NotImplementedError('no zipfile!')
            file = self.__validate_extracted_file(student, file_submission_group, project_root)


            file_submission.file = file 

            return file
    
    def __validate_extracted_file(self, student: Student, file_submission_group: FileSubmissionGroup, extracted_file: Path) -> Path:
        """
        Renames extracted file and sets flags on student if improperly named
        
        :param extracted_file: Path of extracted file not including workspace section
        """
        # Validate naming
        for name in student.name_tokens:
            if name in extracted_file.name:
                break
        else:
            self.logger.error(f'{student.name} improperly named their project directory as {extracted_file.name}')
            file_submission_group.grading_data.proper_naming = False

        # Rename anyways
        extracted_file = Path(self.workspace) / extracted_file
        new_extracted_file = Path(self.workspace) / Path(file_submission_group.get_filename(student))
        if not new_extracted_file.exists():
            extracted_file.rename(new_extracted_file)

        return new_extracted_file
    
class StudentFilterer:

    LEXICOLGRAPHIC_MIN = ''
    LEXICOLGRAPHIC_MAX = '{{{{{{{{{{'

    def __init__(self):
        self.__first_name_begin = self.LEXICOLGRAPHIC_MIN
        self.__first_name_end = self.LEXICOLGRAPHIC_MAX
        self.__last_name_begin = self.LEXICOLGRAPHIC_MIN
        self.__last_name_end = self.LEXICOLGRAPHIC_MAX

    def filter_first_name(self, begin: Optional[str], end: Optional[str]) -> Self:
        if begin:
            self.__first_name_begin = begin.lower()
        if end:
            self.__first_name_end = end.lower()
        return self
    
    def __filter_first_name(self, student: Student) -> bool:
        return self.__first_name_begin <= student.name_tokens[0].lower() <= self.__first_name_end

    def filter_last_name(self, begin: Optional[str], end: Optional[str]) -> Self:
        if begin:
            self.__last_name_begin = begin.lower()
        if end:
            self.__last_name_end = end.lower()
        return self
    
    def __filter_last_name(self, student: Student):
        # Student does not have a last name
        return len(student.name_tokens) == 1 \
        or self.__last_name_begin <= student.name_tokens[-1].lower() <= self.__last_name_end
    
    def filter(self, students: list[Student]) -> list[Student]:
        filtered_students = filter(self.__filter_first_name, students)
        filtered_students = filter(self.__filter_last_name, filtered_students)
        return list(filtered_students)


# Import projects from workspace
# Choose the current project root
# Click all projects
if __name__ == '__main__':
    # Setup

    moodle_session = env.get('MOODLE_SESSION')
    _id = env.get("ID")
    if not moodle_session:
        print("MOODLE_SESSION not found in .env", file=stderr)
        exit(1)
    if not _id:
        print("ID not found in .env", file=stderr)
        exit(1)

    # Installation Services
    moodle_client = MoodleClient(moodle_session=moodle_session, id=_id)
    install_logger = Logger(VERBOSE_DOWNLOAD, 'INSTALL')
    installer = Installer(moodle_client, install_logger, WORKSPACE_DIR)
    student_parser = StudentParser()
    student_filterer = StudentFilterer() # .filter_first_name('binyamin', 'binyamin')

    # Project Validation Services
    project_validation_logger = Logger(VERBOSE_PROJECT_VALIDATION, 'PROJECT VALIDATION')
    project_validator = MavenProjectValidator()
    project = MavenProject(
        Path('../../compiled_testfiles'),
        Path('./target/test-classes'),
        ['AllSequentialTests'],
        Path('./target/surefire-reports/TEST-cs131.pa1.AllSequentialTests.xml'),
        2.5
    )

    # Test Running Services

    test_running_logger = Logger(VERBOSE_TEST_RUNNING, 'TEST RUNNER')

    if INPUT_FILE:
        with open(INPUT_FILE, 'r') as f:
            html = f.read()
    else:
        html = moodle_client.get_html()
    
    if SAVE_HTML:
        with open(SAVE_HTML, 'w') as f:
            f.write(html)

    students = student_parser.parse_html(html)

    if PRINT_ALL_STUDENTS:
        print('======== All Students ========')
        pprint(students)
    students = student_filterer.filter(students)
    if SAFE_MODE:
        print('======== Filtered Students ========')
        pprint(students)
        exit(0)
    for student in students:
        if len(student.submissions) == 0:
            print('=============')
            print(f"{student.name} has no submissions...")

        for submission in student.submissions:
            for file_submission in submission.file_submissions:
                # ==== Installation and Validation ====
                try:
                    maybe_project_root: Optional[Path] = installer.install(student, file_submission, submission, project_validator)
                    if not maybe_project_root:
                        continue
                except Exception as e:
                    install_logger.error(f'Issue with installing \'{student.name}\' submission: {e}')
                    DOWNLOAD_ERRORS.append((student, submission, file_submission, e))
                    continue

                project_root = maybe_project_root

                # ==== Test Running ====
                try:
                    # eclipse.get_tests()
                    results = project.run(project_root)
                    print(results)
                except Exception as e:
                    test_running_logger.error(f'Issue with running \'{student.name}\' tests: {''.join(format_exception(e))}')
                    TEST_RUNNER_ERRORS.append((student, submission, file_submission, e))
                    continue
                    