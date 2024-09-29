
from dataclasses import dataclass

@dataclass
class TestResult:
        tests: int 
        errors: int 
        skipped: int 
        failures: int 