from os import chdir, getcwd, symlink
from typing import Optional
from Atypes import TestCase
import xml.etree.ElementTree as ET
from subprocess import run, DEVNULL, TimeoutExpired
from pathlib import Path
from Atypes import TestResult


class MavenProject:
    def __init__(
        self,
        project: Path,
        project_skeleton: Path,
        test_classes_location: Path,
        tests: list[str],
        test_report_locations: list[Path],
        test_timeout: float,
    ):
        """All paths relative to project root"""
        self.project = project
        self.project_skeleton = project_skeleton
        self.test_classes_location = test_classes_location
        self.tests: list[str] = tests
        self.test_report_locations: list[Path] = test_report_locations
        self.test_timeout: float = test_timeout

    def test(self, project_root: Path) -> list[TestResult]:
        prev_dir = getcwd()
        chdir(project_root)

        try:
            self.__clean_project()
            self.__compile_project()
            self.__link_tests()
            self.__run_all_tests()
            return self.__parse_all_test_reports()
        finally:
            chdir(prev_dir)

    def __clean_project(self):
        if run(["mvn", "clean", "-Dmaven.test.skip"], stdout=DEVNULL).returncode != 0:
            raise RuntimeError("Cleaning Program")

    def __compile_project(self):
        """Compile all files including test files"""
        if run(["mvn", "compile"], stdout=DEVNULL).returncode != 0:
            raise RuntimeError("Compiling Program")

    def __link_tests(self):
        actual_abs = (self.project_skeleton / self.test_classes_location).resolve()
        expected_abs = (self.project / self.test_classes_location).resolve()
        symlink(actual_abs, expected_abs, target_is_directory=True)

    def __run_all_tests(self):
        test_str = ",".join(self.tests)
        try:
            run(["mvn", f"-Dtest={test_str}", "surefire:test"], stdout=DEVNULL, timeout=60)
        except TimeoutExpired as e:
            print("TIMEOUT EXPIRED")
            raise RuntimeError("Timeout Expired")
            
    def __parse_all_test_reports(self):
        test_results = []
        for test_report_location in self.test_report_locations:
            test_results.append(self.__parse_test_report(test_report_location))
        return test_results

    def __parse_test_report(self, test_report_location: Path) -> TestResult:
        test_metadata = ET.parse(test_report_location.absolute()).getroot()
        if test_metadata is None:
            raise RuntimeError(f"Could not find or parse maven test output for {test_report_location}")

        # TODO BEGIN: If a test was skipped figure out what the XML looks like a update this function
        skipped_s: Optional[str] = test_metadata.get("skipped")
        if not skipped_s:
            raise RuntimeError("Could not find # of skipped field")
        try:
            skipped = int(skipped_s)
        except:
            raise RuntimeError("Could not parse skipped field as integer")
        if skipped > 0:
            raise NotImplementedError("TODO: Implement skipped test handling!!!!")
        # TODO END
        testcase_nodes = test_metadata.findall("testcase")

        passing: int
        erroring: int
        skipped: int
        failing: int
        passing_tests: list[TestCase] = []
        erroring_tests: list["TestCase"] = []
        skipped_tests: list["TestCase"] = []
        failing_tests: list["TestCase"] = []
        erroring = int(test_metadata.get("errors")) # type: ignore
        failing = int(test_metadata.get("failures")) # type: ignore
        skipped = int(test_metadata.get("skipped")) # type: ignore
        passing = int(test_metadata.get("tests")) - erroring - failing - skipped # type: ignore
        for testcase_node in testcase_nodes:
            a = testcase_node.attrib
            maybe_failure_node: Optional[ET.Element] = testcase_node.find("failure")
            maybe_error_node: Optional[ET.Element] = testcase_node.find("error")
            maybe_failure_msg: Optional[str] = None
            maybe_error_msg: Optional[str] = None
            if maybe_failure_node is not None:
                maybe_failure_msg = maybe_failure_node.get("message") or maybe_failure_node.get("type")
            if maybe_error_node is not None:
                maybe_error_msg = maybe_error_node.get("message") or maybe_error_node.get("type")
            test_case = TestCase(
                a["name"], a["classname"], a["time"], maybe_failure_msg, maybe_error_msg
            )

            if test_case.failure:
                failing_tests.append(test_case)
            elif test_case.error:
                erroring_tests.append(test_case)
            else:
                passing_tests.append(test_case)
        return TestResult(passing, failing, erroring, skipped, passing_tests, erroring_tests, skipped_tests, failing_tests)
