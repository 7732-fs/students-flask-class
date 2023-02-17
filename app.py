import json
from collections import namedtuple
from sqlite3 import IntegrityError
from setup_db import execute_query
from flask import Flask, redirect, url_for, render_template, request, session, abort

app = Flask(__name__)

app.secret_key="sdksdkj"

def authenticate(username, password):
    role=execute_query(f"SELECT role FROM users WHERE username='{username}' AND password='{password}'")
    if role == []:
        return None
    else:
        return role[0][0]

@app.route('/')
def home():
    return "home sweet home"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        role=authenticate(request.form["username"], request.form["password"])
        if role == None:
            return abort(403)
        else:
            session["role"]=role
            session["username"]=request.form["username"]
    return render_template('login.html')

@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
    if session.get("role", "anonymous")=='admin':
        try:
            execute_query(
                f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
        except IntegrityError:
            return f"{student_id} is already registered to {course_id}"
        return redirect(url_for('registrations', student_id=student_id))
    else:
        return abort(403)
    


@app.route('/registrations/<student_id>')
def registrations(student_id):
    course_names = execute_query(f"""
        SELECT courses.name, courses.teacher_id FROM courses 
        JOIN students_courses on students_courses.course_id=courses.id 
        WHERE students_courses.student_id={student_id} 
    """)
    courses = []
    # challenge: do this in one line!
    for course_tuple in course_names:
        course = namedtuple("Course", ["name", "teacher"])
        course.name = course_tuple[0]
        course.teacher = course_tuple[1]
        courses.append(course)
    return render_template("registrations.html", courses=courses)

# TODO add /registrations endpoint to show all registered students and courses

# for testing: translate from course id to course name


@app.route("/course/<id>")
def course(id):
    name = execute_query(f"SELECT name FROM courses WHERE id={int(id)+1}")
    return json.dumps(name)
