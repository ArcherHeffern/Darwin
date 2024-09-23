# Background 
I am a TA for Brandeis' Operating Systems Course.  

Grading Programming Assignments is a needlessly labor intensive process. Installing and importing all the projects into eclipse takes a long time, clicking through each project's file hierarchies to find the tests takes a while, and switching between excel and eclipse is annoying.  

Since we already have unit tests, we can automate the majority of this process.

# Features
Currently supports downloading all or a filtered range of projects from moodle, parsing all user information for later steps, unzipping projects into the correct directory, and deleting the zip files.  

Supports a variety of options. There is no command line argument parser yet because I'm not yet set on an API

# Planned Features
- Auto running unit tests
    - Since junit outputs raw text, I will need to write a junit test output parser
- Auto grading
- View TODO for the rest of my plans

# Set up
## .env
1. MoodleSession cookie
2. id query string parameter

## Virtual environment
`pip install -r requirements.txt`