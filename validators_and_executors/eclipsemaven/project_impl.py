from os import symlink
from typing import Optional
from bad_config_exception import BadConfigException
from ..project_execution_exception import ProjectExecutionException
import xml.etree.ElementTree as ET
from subprocess import run, DEVNULL
from pathlib import Path
from ..project_I import Project_I
from ..test_result import TestResult


class MavenProject(Project_I):
    def __init__(
            self, 
            compiled_test_classes_actual_location: Path, 
            compiled_test_class_expected_location: Path,
            tests: list[str],
            test_report_location: Path,
            test_timeout: float
            ):
        """All paths relative to project root"""
        if compiled_test_classes_actual_location.is_absolute():
            raise BadConfigException('test classes actual location must be relative to project')
        if compiled_test_class_expected_location.is_absolute():
            raise BadConfigException('test classes expected location must be relative to project')
        if not tests:
            raise BadConfigException('expected list of tests to run')
        if test_report_location.is_absolute():
            raise BadConfigException('test report location must be relative to project')

        self.compiled_test_classes_actual_location: Path = compiled_test_classes_actual_location
        self.compiled_test_classes_expected_location: Path = compiled_test_class_expected_location
        self.tests: list[str] = tests
        self.test_report_location: Path = test_report_location
        self.test_timeout: float = test_timeout
    
    def clean(self):
        if run(['mvn', 'clean'], stdout=DEVNULL).returncode != 0:
            raise ProjectExecutionException('mvn clean')

    def pre_compile_setup(self):
        ...

    def compile_project(self):
        """Does not compile test files"""
        if run(['mvn', 'compile'], stdout=DEVNULL).returncode != 0:
            raise ProjectExecutionException('mvn compile')

    def post_compile_setup(self):
        actual_abs = self.compiled_test_classes_actual_location.resolve()
        expected_abs = self.compiled_test_classes_expected_location.resolve()
        symlink(actual_abs, expected_abs, target_is_directory=True)
    
    def get_tests(self):
        raise NotImplementedError
    
    def run_tests(self) -> TestResult:
        test_str = ','.join(self.tests)
        res = run(['mvn', f'-Dtest={test_str}', 'test'], stdout=DEVNULL)
        # if res.returncode != 0:
        #     raise ProjectExecutionException(f'mvn run tests\n{res.stdout}\n{res.stderr}')

        test_metadata = ET.parse(self.test_report_location.absolute()).getroot()
        if test_metadata is None:
            raise ProjectExecutionException('Could not find or parse maven test output')
        tests_s: Optional[str] = test_metadata.get('tests')
        errors_s: Optional[str] = test_metadata.get('errors')
        skipped_s: Optional[str] = test_metadata.get('skipped')
        failures_s: Optional[str] = test_metadata.get('failures')
        if not tests_s:
            raise ProjectExecutionException('Could not find # of tests field')
        if not errors_s:
            raise ProjectExecutionException('Could not find # of errors field')
        if not skipped_s:
            raise ProjectExecutionException('Could not find # of skipped field')
        if not failures_s:
            raise ProjectExecutionException('Could not find # of failures field')
        
        try:
            tests = int(tests_s)
        except:
            raise ProjectExecutionException('Could not parse tests field as integer')
        try:
            errors = int(errors_s)
        except:
            raise ProjectExecutionException('Could not parse errors field as integer')
        try:
            skipped = int(skipped_s)
        except:
            raise ProjectExecutionException('Could not parse skipped field as integer')
        try:
            failures = int(failures_s)
        except:
            raise ProjectExecutionException('Could not parse failures field as integer')
        return TestResult(tests, errors, skipped, failures)
