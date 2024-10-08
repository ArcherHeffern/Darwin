from darwin.models.client_models import (
    MoodleCourse,
    MoodleCourseParticipant,
    MoodleStudent,
    FileSubmission,
    FileSubmissionGroup,
)
from darwin.midtier.utils import flatmap
from collections import defaultdict
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime
from calendar import Month
from re import match


class MoodleHTMLParser:

    class MoodleHTMLParseError(RuntimeError): ...

    def ajax_get_course(self, text: str) -> MoodleCourse:
        id: int = 0
        name: str = ""
        email: str = ""
        print(text)
        return MoodleCourse(
            name = "",
            participants = []

        )

    def html_get_course(self, html: str) -> MoodleCourse:
        soup = BeautifulSoup(html, features="lxml")
        course_name_n = soup.find("h2")
        if not course_name_n:
            raise self.MoodleHTMLParseError("Could not parse course name")
        course_name = course_name_n.text
        participants: list[MoodleCourseParticipant] = []

        participant_table = soup.findAll('tbody', limit=2)[1]
        if participant_table is None or isinstance(participant_table, NavigableString):
            raise self.MoodleHTMLParseError("Could not find participant table")
        participant_nodes = participant_table.findAll("tr")

        for participant_node in participant_nodes:
            if participant_node['class'] == ['emptyrow']:
                continue
            id: int
            name: str
            email: str

            try:
                id = int(participant_node.td.label['for'].removeprefix("user"))
            except:
                print(participant_node)
                exit()
            name_tag = participant_node.find(class_="cell c1").a
            if (span_tag := name_tag.find('span')) is not None:
                name = ''.join(name_tag.stripped_strings).replace(span_tag.text, '')
            else:
                name = name_tag.text

            email = participant_node.find(class_="cell c2").text
            participants.append(MoodleCourseParticipant(
                id = id,
                name = name,
                email = email,
            ))
        
        return MoodleCourse(
            name = course_name,
            participants=participants
            )

    def html_get_assignment_submissions(self, html: str) -> list[MoodleStudent]:
        soup = BeautifulSoup(html, features="lxml")
        submissions = soup.find_all("tr")
        submissions = filter(self.__check_if_submission, submissions)

        students: list[MoodleStudent] = []

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

            students.append(MoodleStudent(
                sid = sid, 
                name = name, 
                email = email, 
                file_submissions = file_submissions
                ))
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
                FileSubmission(
                    submission_url = submission_url,
                    submission_time = submission_time,
                    )
            )

        file_submission_groups: list[FileSubmissionGroup] = []
        for group_of_file_submissions in time_groups.values():
            file_submission_groups.append(
                FileSubmissionGroup(
                    group_of_file_submissions=group_of_file_submissions
                    )
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
