import uuid
import sqlite3
from datetime import datetime

#connect the database 
conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()

# users = [
#     {"email": "vidunithap@gmail.com", "full_name": "tesgt", "password": "test1234", "auth_provider" : "manual", "theme_preference" : "dark"}
# ]

# for user in users:
#     user_id = str(uuid.uuid4())
#     print(user_id)
#     join_date = datetime.now().isoformat()
#     cursor.execute("""
# INSERT INTO User (user_id, email, full_name, password, auth_provider, theme_preference, join_date) VALUES (?, ?, ?, ?, ?, ?, ?)
# """, (user_id, user["email"], user["full_name"], user["password"], user["auth_provider"], user["theme_preference"], join_date))
#     conn.commit()

# print("done")

courses = [
    {
        "course_name": "Introduction to Python",
        "language_name": "Python",
        "language_image": "images/logos/python_logo.svg",
        "course_image": "images/courses/python_intro_course.jpg"
    },
    {
        "course_name": "Introduction to Javascript",
        "language_name": "JavaScript",
        "language_image": "images/logos/javascript_logo.svg",
        "course_image": "images/courses/javascript_intro_course.jpg"
    },
    {
        "course_name": "Introduction to Typescript",
        "language_name": "TypeScript",
        "language_image": "images/logos/typescript_logo.svg",
        "course_image": "images/courses/typescript_intro_course.jpg"
    },
    {
        "course_name": "Introduction to Java",
        "language_name": "Java",
        "language_image": "images/logos/java_logo.svg",
        "course_image": "images/courses/java_intro_course.jpg"
    },
    {
        "course_name": "Introduction to C++",
        "language_name": "C++",
        "language_image": "images/logos/c++_logo.svg",
        "course_image": "images/courses/c++_intro_course.jpg"
    }
]

for course in courses:
    course_id = str(uuid.uuid4())
    cursor.execute("""
INSERT INTO Course (course_id, course_name, language_image, course_image, language) VALUES (?, ?, ?, ?, ?)
""", (course_id, course["course_name"],  course["language_image"], course["course_image"],course["language_name"]))
    conn.commit()

print("Done")


# guid = str(uuid.uuid4())  

# print(guid)