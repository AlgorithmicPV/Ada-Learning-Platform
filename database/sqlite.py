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


# Python lessons
lessons = [
    {
        "lesson_title": "Welcome to Python Programming",
        "content": """
# Welcome to Python Programming

Welcome to your very first step into the world of programming! This course is designed for complete beginners. By the end of the course, you will be able to write basic Python programs confidently.

**What is Python?**
Python is a widely-used, high-level programming language that is easy to learn due to its readable syntax. It is used for web development, automation, data science, AI, and more.

**Course Structure:**
- Short lessons with explanations
- Code examples
- Small exercises

No prior knowledge is required. Let's get started!
""",
        "lesson_order": 1,
    },
    {
        "lesson_title": "Installing Python and Setting Up Your Environment",
        "content": """
# Installing Python and Setting Up Your Environment

Before we write any Python code, you need to install Python and set up an editor.

**Step 1: Install Python**
1. Go to [https://www.python.org/downloads](https://www.python.org/downloads)
2. Download the latest version for your OS.
3. Install it. Make sure to check **Add Python to PATH** before clicking install.

**Step 2: Choose an Editor**
- You can use any text editor (Notepad, etc.)
- Recommended: [VS Code](https://code.visualstudio.com/) or [Thonny](https://thonny.org/)

**Step 3: Run Python**
- Open your terminal (Command Prompt or Terminal)
- Type: `python` and press Enter
- You should see something like `>>>`. This means Python is ready.
""",
        "lesson_order": 2,
    },
    {
        "lesson_title": "Your First Python Program",
        "content": """
# Your First Python Program

Let's write your very first Python program.

Open your editor and type this:

```python
print("Hello, world!")
```

Save the file as `hello.py`, then run it:

**On Terminal or Command Prompt:**
```bash
python hello.py
```

**Output:**
```
Hello, world!
```

Congratulations! You've just run your first Python program.
""",
        "lesson_order": 3,
    },
    {
        "lesson_title": "Variables and Data Types",
        "content": """
# Variables and Data Types

Variables store data. You can think of them as containers.

```python
name = "Alice"
age = 25
height = 5.6
is_student = True
```

**Common Data Types:**
- `str`: Text (e.g. "Hello")
- `int`: Whole numbers (e.g. 10)
- `float`: Decimal numbers (e.g. 3.14)
- `bool`: Boolean (True or False)

**Print Variables:**
```python
print(name)
print(age)
```
""",
        "lesson_order": 4,
    },
    {
        "lesson_title": "Basic Input and Output",
        "content": """
# Basic Input and Output

**Input:** To get input from a user, use `input()`
```python
name = input("What is your name? ")
print("Hello, " + name + "!")
```

**Output:** We use `print()` to show messages.
```python
print("Welcome to Python!")
```

Everything entered from `input()` is a string by default.
""",
        "lesson_order": 5,
    },
    {
        "lesson_title": "Operators in Python",
        "content": """
# Operators in Python

Operators are used to perform operations on variables and values.

**Arithmetic Operators:**
```python
x = 10
y = 3
print(x + y)  # 13
print(x - y)  # 7
print(x * y)  # 30
print(x / y)  # 3.33
print(x % y)  # 1
```

**Comparison Operators:**
```python
print(x > y)   # True
print(x == y)  # False
```

**Assignment Operators:**
```python
x += 1  # same as x = x + 1
```
""",
        "lesson_order": 6,
    },
    {
        "lesson_title": "Conditional Statements",
        "content": """
# Conditional Statements

Conditional statements let you execute code based on conditions.

```python
age = 18
if age >= 18:
    print("You are an adult")
elif age > 12:
    print("You are a teenager")
else:
    print("You are a child")
```
""",
        "lesson_order": 7,
    },
    {
        "lesson_title": "Loops - for and while",
        "content": """
# Loops - for and while

**For Loop:**
```python
for i in range(5):
    print(i)
```

**While Loop:**
```python
count = 0
while count < 5:
    print(count)
    count += 1
```
""",
        "lesson_order": 8,
    },
    {
        "lesson_title": "Functions",
        "content": """
# Functions

Functions help you reuse code.

```python
def greet(name):
    print("Hello, " + name)

greet("Alice")
```

**Return Values:**
```python
def add(x, y):
    return x + y

result = add(5, 3)
print(result)  # 8
```
""",
        "lesson_order": 9,
    },
    {
        "lesson_title": "Lists and Tuples",
        "content": """
# Lists and Tuples

**List:**
```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])
fruits.append("orange")
```

**Tuple:**
```python
colors = ("red", "green", "blue")
print(colors[1])
```

Lists are mutable, tuples are immutable.
""",
        "lesson_order": 10,
    },
    {
        "lesson_title": "Dictionaries",
        "content": """
# Dictionaries

Dictionaries store data in key-value pairs.

```python
person = {"name": "Alice", "age": 25}
print(person["name"])
person["age"] = 26
```

You can loop through keys:
```python
for key in person:
    print(key, person[key])
```
""",
        "lesson_order": 11,
    },
    {
        "lesson_title": "Working with Files",
        "content": """
# Working with Files

**Writing to a File:**
```python
with open("data.txt", "w") as file:
    file.write("Hello, file!")
```

**Reading from a File:**
```python
with open("data.txt", "r") as file:
    content = file.read()
    print(content)
```
""",
        "lesson_order": 12,
    },
    {
        "lesson_title": "Modules and Libraries",
        "content": """
# Modules and Libraries

A module is a file containing Python code. You can also use built-in libraries.

```python
import math
print(math.sqrt(16))  # 4.0
```

You can also create your own module by saving functions in another `.py` file and importing them.
""",
        "lesson_order": 13,
    },
    {
        "lesson_title": "Error Handling with try/except",
        "content": """
# Error Handling with try/except

Sometimes errors happen in programs. You can use `try` and `except` to handle them safely.

**Example:**
```python
try:
    number = int(input("Enter a number: "))
    result = 10 / number
    print("Result:", result)
except ValueError:
    print("Please enter a valid number.")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

This avoids crashing the program and gives helpful messages.
""",
        "lesson_order": 14,
    },
    {
        "lesson_title": "Introduction to Object-Oriented Programming (OOP)",
        "content": """
# Introduction to Object-Oriented Programming (OOP)

OOP is a way to organize your code using **classes** and **objects**.

**Class = Blueprint**, **Object = Instance of that blueprint**

**Example:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hi, my name is", self.name)

person1 = Person("Alice", 25)
person1.greet()
```

`__init__` is a special method that runs when the object is created.

This makes it easier to manage and scale larger programs.
""",
        "lesson_order": 15,
    },
]

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
