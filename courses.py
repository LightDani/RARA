from connection import get_request

course_api = "https://api.rakamin.com/api/v1/courses/"


def get_courses(api_token):
    user_course_api = "https://api.rakamin.com/api/v1/user_courses"
    headers = {
        "state[]": "expired",
        "state[]": "enrolled",
        "state[]": "completed",
        "disable_pagination": "true",
        "Authorization": f"Bearer {api_token}",
    }
    json_data = get_request(url=user_course_api, headers=headers)

    if json_data:
        courses_name = []
        courses_id = [str(course["course_id"]) for course in json_data["data"]]
        for course_id in courses_id:
            json_data = get_request(url=course_api + course_id, api_token=api_token)
            courses_name.append(json_data["data"]["name"])
        return courses_name, courses_id
    else:
        return exit(1)


def get_live_sessions(course_id, api_token):
    course_data = get_request(url=course_api + course_id)
    topic_id = [i["id"] for i in course_data["data"]["course_modules"]]
    # topic_name = [i["name"] for i in course_data["data"]["course_modules"]]
    module_id, module_name = [], []
    for id in topic_id[-10:]:
        api_url = f"https://api.rakamin.com/api/v1/course_modules/{id}"
        module_data = get_request(api_url, api_token=api_token)
        for module in module_data["data"]["module_sessions"]:
            if module["session_type"] == "live_session":
                module_id.append(module["id"])
                module_name.append(module["name"])
    return module_name, module_id
