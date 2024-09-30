from Atypes import Assignment

assignment_configs: list[Assignment] = []


def new_assignment() -> Assignment: ...


def download(): ...


def grade_all(assignment_config: Assignment): ...
