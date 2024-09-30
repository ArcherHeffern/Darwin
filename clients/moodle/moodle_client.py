from clients.moodle.moodle_parser import StudentParser
from clients.student_filterer import StudentFilterer
from ..client_I import Client_I
import requests
from Atypes import Student, Assignment
from pathlib import Path


class MoodleClient(Client_I):

    url = "https://moodle.brandeis.edu/mod/assign/view.php"

    headers = {
        "Accept": "text/html",
        "Host": "moodle.brandeis.edu",
    }

    def __init__(self, moodle_session: str, id: str, assignment_config: Assignment):

        self.assignment_config: Assignment = assignment_config
        self.parser = StudentParser(assignment_config)

        self.cookies = {
            "MoodleSession": moodle_session,
        }

        self.params = {"id": id, "tifirst": "", "tilast": "", "action": "grading"}

    def get_students(self, student_filterer: StudentFilterer) -> list[Student]:
        r = requests.get(
            url=self.url, params=self.params, headers=self.headers, cookies=self.cookies
        )

        assert r.status_code == 200

        return student_filterer.filter(self.parser.parse_html(r.text))

    def install_file(self, url: str, destination: Path):
        response = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        assert response.status_code == 200

        with open(destination, "wb") as f:
            f.write(response.content)
