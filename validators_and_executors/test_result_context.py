from .test_result import TestResult
from heapq import heappush

class TestResultContext:
    def __init__(self):
        self.test_results: list[TestResult]
    
    def add_test(self, test_result: TestResult):
        heappush(self.test_results, test_result)