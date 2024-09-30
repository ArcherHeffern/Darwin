# TODO
- Ensure all projects are eclipse projects
- Rename to prevent name conflicts and set naming flag

- Use userid in naming project files to prevent name conficts
- Enable filtering subsets of students
- Argument parsing
- In future figure out users workspace dir and add files to the workspace
- Run testing suite
- Data driven scoring system
- When failing a test, keep track, and open a code editor or a view of the codebase for TA to diagnose

# Super late features
- user interface for head TA to assign points
- additional types of scoring eg. Did they do X (Take them to the most likely location)
- Daemon: Continually check if any PA's were uploaded late
- TA pinging system

# Blockers
- Persistant data: How best to flexibly store to either disk, database, or remotely on moodle
Idea: 
1. Create storage interface 
2. What methods does it have? 
3. get_file(file_urn), store_file(course, assignment, student, submission) 


Installing: Just getting the objects
Storing: Persistantly storing Assignment, Grades, etc
Uploading: To moodle

Handling multiple data stores