# Background 
I am a TA for Brandeis' Operating Systems Course.  

Grading Programming Assignments is a needlessly labor intensive process. Installing and importing all the projects into eclipse takes a long time, clicking through each project's file hierarchies to find the tests takes a while, and switching between excel and eclipse is annoying.  

Since we already have unit tests, we can automate the majority of this process.

# Important Branches
1. Darwin API: API for the full stack web app
2. grading_script: Script for running tests locally - Outputs results (passing, failures, errors, failure/error messages) as a text file

Supports a variety of options. There is no command line argument parser yet because I'm not yet set on an API

# Flow 
There are 3 axis to errors, Graded/Ungraded, and Blocking/NonBlocking, Notifying/Non-Notifying

## Overview
PA Configuration -> Student Data Parser -> Project Installer / Validation -> Project Setup / Validation -> Test Runner -> Grader -> Notification System

## Configuration
Head TA Configures settings and uploads test files using web frontend

## Student Submission Metadata Installer
Downloads and parses all student submission metadata. Eg. Submission time, url, student name, etc. Does NOT install the actual submission files.

## Project Installer / Validation
Downloads, unzips, moves projects to workspace directory, and performs basic validations on submissions

### Validations
- Zipped and unzipped file are named correctly
- Checks if submission is an eclipse project (presence of .project and .classpath)
- Eclipse project is located within the topmost directory. If its not eg. 
    - Zipfile is several loose files
    - Project is deeply nested within zipfile
    We attempt to normalize the submission
- Rename all project directories to avoid name conficts

## Project Setup / Validation
1. Parses project configuration files (.project, .classpath, .settings, pom.xml, etc) to deduce how to execute the project.
2. (Optional) Compiles the project
3. Copies actual testfiles into project to prevent student modification of tests

## Test Runner

## TA Notification System

## TA Grading Platform 

## Grader

## Grade Uploader

# Planned Features
- Auto running unit tests
    - Since junit outputs raw text, I will need to write a junit test output parser
- Auto grading
- View TODO for the rest of my plans

# Set up
## .env
1. MoodleSession cookie
2. id query string parameter

## Ant
`brew install ant`

## Virtual environment
`pip install .`

# Running
`fastapi dev application.py`
