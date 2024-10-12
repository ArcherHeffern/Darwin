# Mental Cache
Transition all create methods to return None on error

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
How to approach projections and joins regarding Midtier and Backend Responsibility

Lets say I want to get all students with their names. 
- Create backend endpoint that does the join for me
- How to handle user authentication
- To create my midtier models - Should I a. do API requests in a formatter, only pass data into or b. make requests to another service