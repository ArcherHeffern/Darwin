from Atypes import Assignment, Student, Submission
from bs4 import BeautifulSoup
from datetime import datetime
from calendar import Month
from regex import match
import requests
from Atypes import Student
from pathlib import Path
from itertools import chain

def flatmap(func, *iterable):
    return chain.from_iterable(map(func, *iterable))

class MoodleClient:

    url = "https://moodle.brandeis.edu/mod/assign/view.php"

    headers = {
        "Accept": "text/html",
        "Host": "moodle.brandeis.edu",
    }

    def __init__(self, moodle_session: str, assignment: Assignment):
        self.cookies = {
            "MoodleSession": moodle_session,
        }

        self.params = {"id": assignment.id, "tifirst": "", "tilast": "", "action": "grading"}
        self.assignment = assignment

    def get_students(self) -> list[Student]:
        r = requests.get(
            url=self.url, params=self.params, headers=self.headers, cookies=self.cookies
        )

        assert r.status_code == 200

        return self.__parse_html(r.text)

    def download_file(self, url: str, destination: Path):
        response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        assert response.status_code == 200

        with open(destination, "wb") as f:
            f.write(response.content)


    # ============
    # Parse Utilities
    # ============
    def __parse_html(self, html: str) -> list[Student]:
        soup = BeautifulSoup(html, features="lxml")
        submission_nodes = soup.find_all("tr")
        submission_nodes = filter(self.__check_if_submission, submission_nodes)

        students: list[Student] = []

        for submission_node in submission_nodes:
            sid: int
            name: str
            email: str

            sid = submission_node["class"][0].removeprefix("user")
            name_tokens = [
                t.capitalize()
                for t in submission_node.findChild("td", class_="cell c2").text.split()
            ]
            name = " ".join(name_tokens)
            email = submission_node.findChild("td", class_="cell c3 email").text.strip()
            submitted = self.__has_submission(submission_node)

            submissions: list[Submission] = []
            student = Student(sid, name, name_tokens, email, submissions)

            if submitted:
                submissions = self.__parse_submissions(submission_node, student)

            student.submissions = submissions
            students.append(student)
        return students

    def __parse_submissions(self, submission_node, student: Student) -> list[Submission]:
        submission = submission_node.findChild("td", class_="cell c9")
        file_submission_nodes = submission.findChildren(
            "div", class_="fileuploadsubmission"
        )
        file_submission_time_nodes = submission.findChildren(
            "div", class_="fileuploadsubmissiontime"
        )

        submissions: list[Submission] = []
        for file_submission_node, file_submission_time_node in zip(
            file_submission_nodes, file_submission_time_nodes
        ):
            submission_url: str = file_submission_node.find("a")["href"]
            submission_time: datetime = self.__parse_submission_time(
                file_submission_time_node.text.strip()
            )
            submissions.append(
                Submission(submission_url, submission_time, student, self.assignment, None)
            )

        return submissions
    

    def __parse_submission_time(self, s: str) -> datetime:
        """September 19 2024, 4:11 PM"""
        tokens: list[str] = list(flatmap(lambda s: s.split(":"), flatmap(str.split, s.split(","))))  # type: ignore
        month: int = Month[tokens[0].upper()]
        day: int = int(tokens[1])
        year: int = int(tokens[2])
        hour: int = int(tokens[3])
        minute: int = int(tokens[4])
        period: str = tokens[5]
        if period == "AM":
            ...
        elif period == "PM":
            if hour != 12:
                hour += 12
        else:
            raise ValueError(f"Expected AM or PM but found {period}")
        return datetime(year, month, day, hour, minute)

    def __check_if_submission(self, submission):
        if not submission.get("class"):
            return False
        return match("user\\d+", submission["class"][0])

    def __has_submission(self, submission) -> bool:
        return bool(
            submission.findChild("td", class_="cell c4").findChild(
                "div", class_="submissionstatussubmitted"
            )
        )