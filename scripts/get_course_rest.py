import requests

token = "TODO"
url = "https://moodle.brandeis.edu/webservice/rest/server.php"

params = {
    "wstoken": token,
    "wsfunction": "core_course_get_enrolled_users_by_cmid",
    "moodlewsrestformat": "json",
    "cmid": 433,  # Replace with your course module ID
}


response = requests.post(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
