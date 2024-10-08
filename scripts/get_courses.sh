curl 'https://moodle.brandeis.edu/lib/ajax/service.php?sesskey=TODO' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: MoodleSession=TODO' \
  --data-raw '[{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":0,"classification":"all","sort":"fullname","customfieldname":"","customfieldvalue":""}}]' |
  jq '.[0]["data"]["courses"][0]'