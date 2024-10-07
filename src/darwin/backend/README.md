# About
A lightweight Data Access Layer to backend data types.
No business logic is performed

# Usage
```python
from darwin.backend import Backend
from darwin.models.backend_models import Course, CourseId
from uuid import uuid4

course = Course(
    id = CourseId(uuid4()), 
    name = 'COSI 12b',
    deleted = False
)
Backend.course_dal.create(course)
course = Backend.course_dal.get(CourseId(0))
```
