from models.backend_models import Assignment, Student, FileSubmission, FileSubmissionGroup
from midtier.utils import flatmap
from collections import defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
from calendar import Month
from regex import match


class StudentParser:

    def __init__(self, assignment_config: Assignment):
        self.assignment_config: Assignment = assignment_config

    def parse_html(self, html: str) -> list[Student]:
        soup = BeautifulSoup(html, features="lxml")
        submissions = soup.find_all("tr")
        submissions = filter(self.__check_if_submission, submissions)

        students: list[Student] = []

        for submission in submissions:
            sid: int
            name: str
            email: str
            file_submissions: list[FileSubmissionGroup]

            sid = submission["class"][0].removeprefix("user")
            name_tokens = [
                t.capitalize()
                for t in submission.findChild("td", class_="cell c2").text.split()
            ]
            name = " ".join(name_tokens)
            email = submission.findChild("td", class_="cell c3 email").text.strip()
            submitted = self.__has_submission(submission)

            if submitted:
                file_submissions = self.__parse_submissions(submission)
            else:
                file_submissions = []

            students.append(Student(sid, name, name_tokens, email, file_submissions))
        return students

    def __parse_submissions(self, submission) -> list[FileSubmissionGroup]:
        submission = submission.findChild("td", class_="cell c9")
        file_submission_nodes = submission.findChildren(
            "div", class_="fileuploadsubmission"
        )
        file_submission_time_nodes = submission.findChildren(
            "div", class_="fileuploadsubmissiontime"
        )

        time_groups: defaultdict[datetime, list[FileSubmission]] = defaultdict(list)
        for file_submission_node, file_submission_time_node in zip(
            file_submission_nodes, file_submission_time_nodes
        ):
            submission_url: str = file_submission_node.find("a")["href"]
            submission_time: datetime = self.__parse_submission_time(
                file_submission_time_node.text.strip()
            )
            time_groups[submission_time].append(
                FileSubmission(submission_url, submission_time)
            )

        file_submission_groups: list[FileSubmissionGroup] = []
        for group_of_file_submissions in time_groups.values():
            file_submission_groups.append(
                FileSubmissionGroup(group_of_file_submissions, self.assignment_config)
            )

        return file_submission_groups

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
