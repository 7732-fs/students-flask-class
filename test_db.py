from setup_db import create_tables, create_fake_data, execute_query
import requests

# pytest example


def test_db():
    create_tables()
    create_fake_data(students_num=20)
    num = int(execute_query("SELECT COUNT(id) FROM students")[0][0])
    assert num == 20


def test_registration():
    course_id = 4
    r = requests.get(f"http://127.0.0.1:5000/register/1/{course_id}")
    if r.status_code == 200:
        r = requests.get("http://127.0.0.1:5000/registrations/1")
        name = requests.get(
            f"http://127.0.0.1:5000/course/{course_id}").json()[0][0]
        assert r.text.find(name) != -1
    assert r.status_code==403
