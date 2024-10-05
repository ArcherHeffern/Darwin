from sqlite3 import Connection
from typing import Any

from src.darwin.models.backend_models import Assignment, AssignmentId


class AssignmentDal:
    def __init__(self, c: Connection):
        self.c = c
    
    def get_all(self):
        c = self.c
        with c:
            res: list[Any] = c.execute("""
            --sql
            SELECT * FROM assignment;
            """).fetchall()

        return res
    

    def create(self, assignment: Assignment):
        c = self.c
        with c:
            c.execute("""
            --sql
            INSERT INTO assignment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                assignment.id,
                assignment.course_f,
                assignment.name,
                assignment.due_date,
                assignment.project_type_f,
                assignment.source_type,
                assignment.source_reference,
                assignment.assignment_stub_location_type_f, 
                assignment.assignment_stub_reference,
                assignment.assignment_testfiles_location_type_f,
                assignment.assignment_testfiles_reference,
                assignment.last_downloaded,
                assignment.deleted, 
                  ))

    # id: AssignmentId
    # course_f: CourseId
    # name: str
    # due_date: datetime
    # project_type_f: "ProjectType"
    # source_type: "SourceType"
    # source_reference: str
    # assignment_stub_location_type_f: "BlobLocationType"
    # assignment_stub_reference: str
    # assignment_testfiles_location_type_f: "BlobLocationType"
    # assignment_testfiles_reference: str
    # last_downloaded: Optional[str]
    # deleted: bool
