import requests
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
from typing import Optional
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

# ======== Runtime Errors ========
DOWNLOAD_ERRORS: list[tuple['Student', 'FileSubmissionGroup', 'FileSubmission', Exception]] = []
# TEST_RUNNER: dict[tuple['Student', 'FileSubmission', 'FileSubmissionGroup'], str] = {}

env = dotenv.dotenv_values()
pprint = PrettyPrinter().pprint

class Logger:
    def __init__(self, enabled: bool):
        self.enabled = enabled
    
    def log(self, s: str):
        if self.enabled:
            print(s)
    
    def error(self, s: str):
        if self.enabled:
            print(f"{Fore.RED}{s}{Style.RESET_ALL}", file=stderr)

@dataclass
class Lateness:
    days: int
    hours: int
    minutes: int
    seconds: int

    literal: Optional[str] = None # For debug purposes

    @staticmethod
    def from_str(s: str) -> Optional['Lateness']:
        days = 0
        hours = 0
        minutes = 0
        seconds = 0

        m: Match|None

        # May have to account for months in the future

        # Try parse days late
        # \d\d? days? \d\d? hours? late
        if ( m := match('(\\d\\d?) days? (\\d\\d?) hours? late', s) ):
            days = int(m.group(1))
            hours = int(m.group(2))

        # Try parse hours late
        # \d\d? hours? \d\d? mins? late
        elif ( m:= match('(\\d\\d?) hours? (\\d\\d?) mins? late', s) ):
            hours = int(m.group(1))
            minutes = int(m.group(2))
            
        # Try parse minutes late
        # \d\d? mins? \d\d? secs? late
        elif ( m:= match('(\\d\\d?) mins? (\\d\\d?) secs? late', s) ):
            minutes = int(m.group(1))
            seconds = int(m.group(2))

        # Try parse seconds late
        # \d\d? secs? late
        elif ( m:= match('(\\d\\d?) secs? late', s) ):
            seconds = int(m.group(1))
        
        else:
            raise Exception(f"Expected date {s} to follow format")

        return Lateness(days, hours, minutes, seconds, s)
    
    def __bool__(self):
        return bool(self.days or self.hours or self.minutes or self.seconds)

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
    
    def __parse_lateness(self, submission) -> Optional[Lateness]:
        if not self.__has_submission(submission):
            return None
        late_submission_node = submission.findChild("div", class_='latesubmission')
        if not late_submission_node:
            return Lateness(0, 0, 0, 0)

        late_submission_text = late_submission_node.text.strip()
        return Lateness.from_str(late_submission_text)

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
    
    def install_java_project(self, student: Student, file_submission: FileSubmission, file_submission_group: FileSubmissionGroup) -> Optional[Path]:
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

        file_path = Path(self.workspace) / file_submission_group.get_filename(student)
        zip_file_path = Path(self.workspace) / (file_submission_group.get_filename(student) + ".zip")

        self.moodle_client.install_file(file_submission.download_url, zip_file_path)

        with self.FileManager(zip_file_path): # Deletes zipfile when leaving function scope
            l.log('=============')
            if is_zipfile(zip_file_path):
                with ZipFile(zip_file_path, 'r') as zip_ref:
                    l.log(f'{student.name} zipfile')
                    dot_project_files = [x for x in zip_ref.namelist() if '.project' == Path(x).name]
                    if not len(dot_project_files):
                        raise Exception('.project file not found - Not an eclipse project')

                    # Extract the project depending on how project was zipped
                    dot_project_file = Path(dot_project_files[0])
                    num_parts = len(dot_project_file.parts)
                    extracted_file: Path
                    if num_parts == 2:
                        extracted_file = Path(dot_project_file.parts[0])
                        zip_ref.extractall(self.workspace)
                    elif num_parts == 1:
                        raise NotImplementedError('.project is zipped without a root directory')
                    else:
                        raise NotImplementedError(f'.project is deeply nested in zip file located at {dot_project_file}')

                file = self.__validate_extracted_file(student, file_submission_group, extracted_file)
            else:
                raise NotImplementedError('no zipfile!')

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
    def filter_last_name(self, students: list[Student], _min: str = "", _max: str = "{") -> list[Student]:
        _min = _min.lower()
        _max = _max.lower()
        new_students = []
        for student in students:
            name = student.name.split()[-1].lower()
            if _min <= name <= _max:
                new_students.append(student)
        return new_students

class TestRunner:
    def __init__(self):
        # TODO: Allow for uploading the test dir
        ...

    def compile_project(self):
        ...
    
    def run_tests(self, project_root: Path):
        abs_project_root = project_root.absolute()
        classpath = [
        f'{abs_project_root}/target/test-classes',
        f'{abs_project_root}/target/classes',
        '/Users/archerheffern/.m2/repository/junit/junit/4.12/junit-4.12.jar', 
        '/Users/archerheffern/.m2/repository/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar',
        ]

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

    moodle_client = MoodleClient(moodle_session=moodle_session, id=_id)
    install_logger = Logger(VERBOSE_DOWNLOAD)
    installer = Installer(moodle_client, install_logger, WORKSPACE_DIR)
    student_parser = StudentParser()
    student_filterer = StudentFilterer()

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
    students = student_filterer.filter_last_name(students, "he", "he")
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
                # ==== Installation ====
                try:
                    maybe_project_path: Optional[Path] = installer.install_java_project(student, file_submission, submission)
                    if not maybe_project_path:
                        continue
                except Exception as e:
                    install_logger.error(f'Issue with \'{student.name}\' submission: {e}')
                    DOWNLOAD_ERRORS.append((student, submission, file_submission, e))
                    continue

                # ==== Test Running ====
                project_path = maybe_project_path

    # pprint(DOWNLOAD_ERRORS)
