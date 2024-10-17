# Usage
1. Set up virtual environment and pip install dependencies
``` bash
python3.12 -m venv .venv
source .venv/bin/activate
pip3.12 install -r requirements.txt
```
2. Create .env file with assignment ID and MOODLE_SESSION
 - Get ID from assignment url on moodle from the query string parameter
 - Get MOODLE_SESSION from moodle cookies
3. Move compiled test classfiles to ./compiled_testfiles - Compile by downloading project and running mvn compile within the project
4. Modify PA context located at top of auto_grader.py
5. Modify range of students graded by calling relevent methods on StudentFilterer class in auto_grader.py
Example: 
```python
student_filterer = StudentFilterer().filter_last_name("heffern", "tern")
```
5. Run auto_grader
`python3.12 auto_grader.py`

# Background 
I am a TA for Brandeis' Operating Systems Course.  

Grading Programming Assignments is a needlessly labor intensive process. Installing and importing all the projects into eclipse takes a long time, clicking through each project's file hierarchies to find the tests takes a while, and switching between excel and eclipse is annoying.  

Since we already have unit tests, we can automate the majority of this process.

# Features
Currently supports downloading all or a filtered range of projects from moodle, parsing all user information for later steps, unzipping projects into the correct directory, deleting the zip files, running tests, and outputting test results as a text file