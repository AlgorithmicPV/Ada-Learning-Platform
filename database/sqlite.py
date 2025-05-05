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

challenges = [
    # Easy
    {
        "question_number": 1,
        "challenge_title": "Print Hello World",
        "question": "**Description**:\nWrite a program that prints `Hello, World!` to the console.\n\n**Tips**:\n- Use the `print()` function.\n- Make sure the output matches exactly.",
        "status": "unattempted",
        "difficulty_level": "easy"
    },
    {
        "question_number": 2,
        "challenge_title": "Odd or Even",
        "question": "**Description**:\nWrite a function that checks whether a given integer is odd or even.\n\n**Tips**:\n- Use the modulo operator `%` to check divisibility.\n- Return or print a clear message like 'Odd' or 'Even'.",
        "status": "unattempted",
        "difficulty_level": "easy"
    },
    {
        "question_number": 3,
        "challenge_title": "Sum of List",
        "question": "**Description**:\nCreate a function that takes a list of numbers and returns the sum.\n\n**Tips**:\n- Use a loop or built-in functions.\n- Handle empty lists gracefully.",
        "status": "unattempted",
        "difficulty_level": "easy"
    },

    # Medium
    {
        "question_number": 4,
        "challenge_title": "Fibonacci Sequence Generator",
        "question": "**Description**:\nWrite a function that returns the first N numbers in the Fibonacci sequence.\n\n**Tips**:\n- Start with 0 and 1.\n- Each number is the sum of the previous two.\n- Use a loop or recursion.",
        "status": "unattempted",
        "difficulty_level": "medium"
    },
    {
        "question_number": 5,
        "challenge_title": "Palindrome Checker",
        "question": "**Description**:\nCreate a function to check if a given string is a palindrome (it reads the same forwards and backwards).\n\n**Tips**:\n- Ignore spaces and capitalization.\n- Consider using string slicing or built-in functions.",
        "status": "unattempted",
        "difficulty_level": "medium"
    },
    {
        "question_number": 6,
        "challenge_title": "Prime Number Generator",
        "question": "**Description**:\nGenerate all prime numbers less than a given number N.\n\n**Tips**:\n- A prime number is only divisible by 1 and itself.\n- Use nested loops or the Sieve of Eratosthenes.",
        "status": "unattempted",
        "difficulty_level": "medium"
    },

    # Hard
    {
        "question_number": 7,
        "challenge_title": "Merge Overlapping Intervals",
        "question": "**Description**:\nGiven a list of intervals (like `[1,3]`, `[2,6]`), merge all overlapping intervals.\n\n**Tips**:\n- Sort the intervals first.\n- Compare current and next interval to decide if they overlap.",
        "status": "unattempted",
        "difficulty_level": "hard"
    },
    {
        "question_number": 8,
        "challenge_title": "LRU Cache Design",
        "question": "**Description**:\nDesign a Least Recently Used (LRU) cache that supports `get()` and `put()` operations in O(1) time.\n\n**Tips**:\n- Use a combination of a hash map and a doubly linked list.\n- Understand how cache eviction works when capacity is exceeded.",
        "status": "unattempted",
        "difficulty_level": "hard"
    },
    {
        "question_number": 9,
        "challenge_title": "Word Ladder Path Finder",
        "question": "**Description**:\nTransform a start word into an end word by changing one letter at a time. Each transformed word must exist in the given dictionary.\n\n**Tips**:\n- Use BFS (Breadth-First Search) to find the shortest path.\n- Keep track of visited words to avoid loops.",
        "status": "unattempted",
        "difficulty_level": "hard"
    }
]


for challenge in challenges:
    challenge_id = str(uuid.uuid4())
    cursor.execute(
        """
INSERT INTO Challenge (challenge_id, number, challenge_title, question, status, difficulty_level) VALUES (?, ?, ?, ?, ?, ?)
""",
        (
            challenge_id,
            challenge["question_number"],
            challenge["challenge_title"],
            challenge["question"],
            challenge["status"],
            challenge["difficulty_level"],
        ),
    )
    conn.commit()

print("done")
