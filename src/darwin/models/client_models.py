from dataclasses import dataclass


@dataclass
class MoodleScrapeResults:
    assignmentid: int
    classid: int
    results: list["MoodleScrapeResult"]


@dataclass
class MoodleScrapeResult:
    sid: int  # Student id
    classid: int  # Class id
