from darwin.backend.services import course, assignment
from darwin.backend.dal import Dal

class Backend:
    dal = Dal
    course_service = course.CourseService()
    assignment_service = assignment.AssignmentService()