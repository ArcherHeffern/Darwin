import requests
import dotenv
from pprint import PrettyPrinter
from zipfile import ZipFile
from os import remove, makedirs
from sys import stderr
from pathlib import Path
from regex import Match, match
from bs4 import BeautifulSoup
from typing import Optional
from dataclasses import dataclass

# FILENAME = 'people'
# WORKSPACE_DIR = '.'
WORKSPACE_DIR = '/Users/archerheffern/fall2024OS_pa1/'
PA_NUMBER = 1
SAVE_HTML: Optional[str] = None
PRINT_ALL_STUDENTS = False # Prints all students scraped from html
SAFE_MODE = True # Does not install anything - Instead prints students specified by your range
INPUT_FILE: Optional[str] = None

env = dotenv.dotenv_values()

pprint = PrettyPrinter().pprint

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

        m: Match

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
class Student:
    name: str # Capitalized
    name_tokens: list[str] # Each capitalized
    email: str
    submission_name: Optional[str]
    submission_url: Optional[str]

    # Grading data
    late: Optional[Lateness] # None if not submitted
    eclipse_project: bool = True
    proper_naming: bool = True
    
    grade: int = 0


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
            name: str
            email: str
            late: Optional[Lateness] = None
            submission_name: Optional[str] = None
            submission_url: Optional[str] = None

            name_tokens = [t.capitalize() for t in submission.findChild("td", class_='cell c2').text.split()] # .string.split()
            name = " ".join(name_tokens)
            email = submission.findChild("td", class_='cell c3 email').text.strip()
            late = self.__parse_lateness(submission)
            if late is not None:
                submission_node = submission.findChild("div", class_='fileuploadsubmission').find('a')
                submission_name = submission_node.text
                submission_url = submission_node['href']
            
            students.append(Student(name, name_tokens, email, submission_name, submission_url, late))
        return students
            

    def __check_if_submission(self, submission):
        if not submission.get('class'):
            return False
        return match("user\\d+", submission['class'][0])


    def __parse_lateness(self, submission) -> Optional[Lateness]:
        is_submitted = bool(submission.findChild("td", class_='cell c4').findChild('div', class_='submissionstatussubmitted'))
        if not is_submitted:
            return None
        late_submission_node = submission.findChild("div", class_='latesubmission')
        if not late_submission_node:
            return Lateness(0, 0, 0, 0)

        late_submission_text = late_submission_node.text.strip()
        return Lateness.from_str(late_submission_text)

class Installer:
    def __init__(self, moodle_client: MoodleClient, workspace: str = '.'):
        self.moodle_client = moodle_client
        self.workspace = workspace
    
    def install(self, student: Student) -> Path:
        """Installs zipfile, extracts it, deletes the zipfile, and returns the filename"""
        assert student.late is not None, "Student has no submission so there is nothing to install"
        filename = "".join(student.name_tokens) + "_PA" + str(PA_NUMBER)
        zip_file_path = Path(self.workspace) / (filename + ".zip")
        makedirs(self.workspace, exist_ok=True)
        self.moodle_client.install_file(student.submission_url, zip_file_path)
        with ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.workspace)
        remove(zip_file_path)

        # Rename to prevent name conflicts and set naming flag
        # In future figure out users workspace dir and add files to the workspace

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
    ...

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
    installer = Installer(moodle_client, WORKSPACE_DIR)
    student_parser = StudentParser()
    student_filterer = StudentFilterer()

    if INPUT_FILE:
        with open('testing.html', 'r') as f:
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
    students = student_filterer.filter_last_name(students, "egleston", "egleston")
    if SAFE_MODE:
        print('======== Filtered Students ========')
        pprint(students)
        exit(0)
    for student in students:
        if student.late is None:
            print(f"Skipping {student.name}...")
            continue

        project_path = installer.install(student)