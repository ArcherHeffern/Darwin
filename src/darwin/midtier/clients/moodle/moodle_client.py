from darwin.midtier.clients.moodle.moodle_parser import MoodleHTMLParser
from darwin.models.client_models import MoodleCourse, MoodleStudent
import requests
from pathlib import Path


class MoodleClient:

    __course_url = "https://moodle.brandeis.edu/course/view.php?"
    __course_users_url = "https://moodle.brandeis.edu/user/index.php"
    __assignment_url = "https://moodle.brandeis.edu/mod/assign/view.php?id="
    __ajax_services_endpoint = "https://moodle.brandeis.edu/lib/ajax/service.php"
    MAX_COURSE_SIZE = 300

    __headers = {
        "Accept": "text/html",
        "Host": "moodle.brandeis.edu",
    }

    def __init__(self, moodle_session: str):

        self.__parser = MoodleHTMLParser()
        self.__cookies = {
            "MoodleSession": moodle_session,
        }

    def html_get_course(self, course_id: str) -> MoodleCourse:
        params = {
            "id": course_id,
            "perpage": self.MAX_COURSE_SIZE,
            "tifirst": "",
            "tilast": "",
        }
        r = requests.get(
            url=self.__course_users_url,
            params=params,
            headers=self.__headers,
            cookies=self.__cookies,
        )

        assert r.status_code == 200

        return self.__parser.html_get_course(course_id, r.text)

    def html_get_assignment(self, assignment_id: int) -> list[MoodleStudent]:
        params = {"id": assignment_id, "tifirst": "", "tilast": "", "action": "grading"}
        r = requests.get(
            url=self.__assignment_url,
            params=params,
            headers=self.__headers,
            cookies=self.__cookies,
        )

        assert r.status_code == 200

        return self.__parser.html_get_assignment_submissions(r.text)

    def install_file(self, url: str, destination: Path):
        response = requests.get(url=url, headers=self.__headers, cookies=self.__cookies)
        assert response.status_code == 200

        with open(destination, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    from darwin.config import Config

    print(
        len(
            MoodleClient(Config.MOODLE_SESSION)
            .html_get_course(Config.COURSE_ID)
            .participants
        )
    )
