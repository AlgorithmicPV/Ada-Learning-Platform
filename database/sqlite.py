import uuid
import sqlite3
from datetime import datetime

# connect the database
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

# courses = [
#     {
#         "course_name": "Introduction to Python",
#         "language_name": "Python",
#         "language_image": "images/logos/python_logo.svg",
#         "course_image": "images/courses/python_intro_course.jpg"
#     },
#     {
#         "course_name": "Introduction to Javascript",
#         "language_name": "JavaScript",
#         "language_image": "images/logos/javascript_logo.svg",
#         "course_image": "images/courses/javascript_intro_course.jpg"
#     },
#     {
#         "course_name": "Introduction to Typescript",
#         "language_name": "TypeScript",
#         "language_image": "images/logos/typescript_logo.svg",
#         "course_image": "images/courses/typescript_intro_course.jpg"
#     },
#     {
#         "course_name": "Introduction to Java",
#         "language_name": "Java",
#         "language_image": "images/logos/java_logo.svg",
#         "course_image": "images/courses/java_intro_course.jpg"
#     },
#     {
#         "course_name": "Introduction to C++",
#         "language_name": "C++",
#         "language_image": "images/logos/c++_logo.svg",
#         "course_image": "images/courses/c++_intro_course.jpg"
#     }
# ]

# for course in courses:
#     course_id = str(uuid.uuid4())
#     cursor.execute("""
# INSERT INTO Course (course_id, course_name, language_image, course_image, language) VALUES (?, ?, ?, ?, ?)
# """, (course_id, course["course_name"], course["language_image"], course["course_image"], course["language_name"]))
#     conn.commit()

# print("Done")


# guid = str(uuid.uuid4())

# print(guid)

python_course_id = "7da7fd5f-8ff3-4ef7-9431-20c42961f16e"
javascript_course_id = "2b3ae171-3168-4c52-b2f6-5c318ced669a"
typescript_course_id = "2d9673df-902f-4771-ae46-703475f40f8d"
java_course_id = "dac91fc1-e6f7-4973-8ae8-b81e0047aa2b"
cplusplus_course_id = "cc676ca0-cf8d-4370-bf19-4625bd322b02"



for lesson in lessons:
    lesson_id = str(uuid.uuid4())
    cursor.execute(
        """
INSERT INTO Lesson (lesson_id, course_id, lesson_title, content, lesson_order) VALUES (?, ?, ?, ?, ?)
""",
        (
            lesson_id,
            python_course_id,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
