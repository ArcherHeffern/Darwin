# Background 
I am a TA for Brandeis' Operating Systems Course.  

Grading Programming Assignments is a needlessly labor intensive process. Installing and importing all the projects into eclipse takes a long time, clicking through each project's file hierarchies to find the tests takes a while, and switching between excel and eclipse is annoying.  

Since we already have unit tests, we can automate the majority of this process.

# Important Branches
1. Darwin API: API for the full stack web app
2. grading_script: Script for running tests locally
   Outputs results (passing, failures, errors, failure/error messages) as a text file
   View grading_script README for usage. 

# Darwin API
## Features
- Authentication (Sign up, sign in) with Email verification using SMTP, OAuth protocol, hashed passwords, and revokable / expiring tokens
- Admin Panel to manage users and assignments
- Data access control - Read, Write, and Delete permissions for all data
- Course management
- Pulling of courses from Moodle
- Pulling of assignments from Moodle
- A lot of other things I'm forgetting...

## Tech Stack
python, sqlalchemy, sqlite3, fastapi
I intentionally keep very few dependencies to minimize costs for the CS department when I leave

## Architecture
- Backend data access layer
- Miditer presentation layer

## Set Up
```bash
python3.12 -m venv .venv # Create virtual environment
source .venv/bin/activate # Activate virtual environment
pip3.12 install -e . # install dependencies
```

## Running
View scripts folder for options

# Flow
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


## Virtual environment
`pip install .`

# Running
`fastapi dev application.py`
