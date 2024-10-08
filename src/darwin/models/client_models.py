from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class MoodleCourse(BaseModel):
    id: int
    name: str
    participants: list["MoodleCourseParticipant"]


class MoodleCourseParticipant(BaseModel):
    id: int
    name: str
    email: str
    role: 'MoodleCourseParticipantRole'


class MoodleCourseParticipantRole(Enum):
    STUDENT = "Student"
    INSTRUCTOR = "Instructor"
    NONE = "No roles"


class MoodleStudent(BaseModel):
    sid: int  # Moodle assigned student ID
    name: str
    email: str
    file_submissions: list["FileSubmissionGroup"]


class FileSubmissionGroup(BaseModel):
    group_of_file_submissions: list["FileSubmission"]


class FileSubmission(BaseModel):
    submission_url: str
    submission_time: datetime
