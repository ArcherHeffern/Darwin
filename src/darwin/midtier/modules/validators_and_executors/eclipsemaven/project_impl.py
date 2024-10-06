from os import symlink
from typing import Optional
from models.backend_models import (
    BadConfigException,
    ProjectExecutionException,
    TestCase,
)
import xml.etree.ElementTree as ET
from subprocess import run, DEVNULL
from pathlib import Path
from ..project_I import Project_I
from models.backend_models import TestResult


class MavenProject(Project_I):
    def __init__(
        self,
        compiled_test_classes_actual_location: Path,
        compiled_test_class_expected_location: Path,
        tests: list[str],
        test_report_location: Path,
        test_timeout: float,
    ):
        """All paths relative to project root"""
        if not compiled_test_classes_actual_location.is_absolute():
            raise BadConfigException("test classes actual location but be absolute")
        if compiled_test_class_expected_location.is_absolute():
            raise BadConfigException(
                "test classes expected location must be relative to project"
            )
        if not tests:
            raise BadConfigException("expected list of tests to run")
        if test_report_location.is_absolute():
            raise BadConfigException("test report location must be relative to project")

        self.compiled_test_classes_actual_location: Path = (
            compiled_test_classes_actual_location
        )
        self.compiled_test_classes_expected_location: Path = (
            compiled_test_class_expected_location
        )
        self.tests: list[str] = tests
        self.test_report_location: Path = test_report_location
        self.test_timeout: float = test_timeout

    def clean(self):
        if run(["mvn", "clean"], stdout=DEVNULL).returncode != 0:
            raise ProjectExecutionException("mvn clean")

    def pre_compile_setup(self): ...

    def compile_project(self):
        """Does not compile test files"""
        if run(["mvn", "compile"], stdout=DEVNULL).returncode != 0:
            raise ProjectExecutionException("mvn compile")

    def post_compile_setup(self):
        actual_abs = self.compiled_test_classes_actual_location.resolve()
        expected_abs = self.compiled_test_classes_expected_location.resolve()
        symlink(actual_abs, expected_abs, target_is_directory=True)

    def get_tests(self):
        raise NotImplementedError

    def run_tests(self) -> TestResult:
        test_str = ",".join(self.tests)
        run(["mvn", f"-Dtest={test_str}", "test"], stdout=DEVNULL)
        test_metadata = ET.parse(self.test_report_location.absolute()).getroot()
        if test_metadata is None:
            raise ProjectExecutionException("Could not find or parse maven test output")

        # TODO BEGIN: If a test was skipped figure out what the XML looks like a update this function
        skipped_s: Optional[str] = test_metadata.get("skipped")
        if not skipped_s:
            raise ProjectExecutionException("Could not find # of skipped field")
        try:
            skipped = int(skipped_s)
        except:
            raise ProjectExecutionException("Could not parse skipped field as integer")
        if skipped > 0:
            raise NotImplementedError("TODO: Implement skipped test handling!!!!")
        # TODO END
        testcase_nodes = test_metadata.findall("testcase")

        passing_tests: list[TestCase] = []
        erroring_tests: list["TestCase"] = []
        skipped_tests: list["TestCase"] = []
        failing_tests: list["TestCase"] = []
        for testcase_node in testcase_nodes:
            a = testcase_node.attrib
            maybe_failure_node: Optional[ET.Element] = testcase_node.find("failure")
            maybe_error_node: Optional[ET.Element] = testcase_node.find("error")
            maybe_failure_msg: Optional[str] = None
            maybe_error_msg: Optional[str] = None
            if maybe_failure_node is not None:
                maybe_failure_msg = maybe_failure_node.get("message")
            if maybe_error_node is not None:
                maybe_error_msg = maybe_error_node.get("message")
            test_case = TestCase(
                a["name"], a["classname"], a["time"], maybe_failure_msg, maybe_error_msg
            )

            if test_case.failure:
                failing_tests.append(test_case)
            elif test_case.error:
                erroring_tests.append(test_case)
            else:
                passing_tests.append(test_case)
        return TestResult(passing_tests, erroring_tests, skipped_tests, failing_tests)
