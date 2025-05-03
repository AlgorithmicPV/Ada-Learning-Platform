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

lessons = [
    {
        "lesson_title": "Welcome to C++ Programming",
        "content": """
# Welcome to C++ Programming

Hey there! 👋 Ready to dive into C++?

C++ is a powerful programming language used in everything from game engines to operating systems. It’s fast, flexible, and teaches you how computers really work.

### Why learn C++?
- It's widely used in performance-critical applications
- It builds strong programming fundamentals
- It’s the foundation for many other languages

This course is designed for total beginners. No experience? No worries. We’ll guide you step by step.
""",
        "lesson_order": 1
    },
    {
        "lesson_title": "Setting Up C++",
        "content": """
# Setting Up C++

Before we can start coding, let’s set up your environment.

### Option 1: Using an online compiler (easiest)
- Go to [https://www.onlinegdb.com/online_c++_compiler](https://www.onlinegdb.com/online_c++_compiler)
- Select "C++" and start coding right away in your browser

### Option 2: Install locally
1. Download and install a C++ compiler:
   - Windows: Install [Code::Blocks](http://www.codeblocks.org/downloads) or [MinGW](https://osdn.net/projects/mingw/releases/)
   - Mac: Use Xcode or install `g++` via Homebrew
   - Linux: Use `sudo apt install g++`

2. Use any text editor or IDE like:
   - VS Code
   - CLion
   - Code::Blocks

### Check your installation
Run:
```bash
g++ --version
```
If you see a version number, you’re ready!
""",
        "lesson_order": 2
    },
    {
        "lesson_title": "Your First C++ Program",
        "content": """
# Your First C++ Program

Let’s write a simple program that prints a message.

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
    return 0;
}
```

### Explanation:
- `#include <iostream>` lets us use `cout` for printing
- `using namespace std;` avoids typing `std::cout`
- `int main()` is where the program starts
- `cout <<` prints to the screen
- `endl` ends the line
- `return 0;` signals successful execution

### How to run:
1. Save as `hello.cpp`
2. Compile with:
```bash
g++ hello.cpp -o hello
```
3. Run it:
```bash
./hello
```

🎉 It should print `Hello, world!`
""",
        "lesson_order": 3
    },
    {
        "lesson_title": "Variables and Data Types",
        "content": """
# Variables and Data Types

Variables store data. In C++, you need to declare the type.

```cpp
int age = 25;
double height = 5.9;
char grade = 'A';
bool isStudent = true;
```

### Explanation:
- `int` for whole numbers
- `double` for decimals
- `char` for single characters
- `bool` for true/false

You can print them:
```cpp
cout << "Age: " << age << endl;
```

Declaring types helps the computer understand your program better.
""",
        "lesson_order": 4
    },
    {
        "lesson_title": "User Input",
        "content": """
# User Input

Use `cin` to get input from the user.

```cpp
#include <iostream>
using namespace std;

int main() {
    string name;
    int age;

    cout << "Enter your name: ";
    cin >> name;

    cout << "Enter your age: ";
    cin >> age;

    cout << "Hello, " << name << ". You are " << age << " years old." << endl;
    return 0;
}
```

### Explanation:
- `cin >>` reads input from the user
- It stores the value in the variable you specify

This makes your programs interactive!
""",
        "lesson_order": 5
    },
    {
        "lesson_title": "If Statements",
        "content": """
# If Statements

Use `if` to run code based on conditions.

```cpp
int age = 17;

if (age >= 18) {
    cout << "You are an adult." << endl;
} else {
    cout << "You are a minor." << endl;
}
```

### Explanation:
- The condition inside `if (...)` is checked
- If it’s true, the first block runs
- Otherwise, the `else` block runs

You can add more with `else if`:
```cpp
if (age >= 65) {
    cout << "Senior." << endl;
} else if (age >= 18) {
    cout << "Adult." << endl;
} else {
    cout << "Minor." << endl;
}
```
""",
        "lesson_order": 6
    },
    {
        "lesson_title": "Loops",
        "content": """
# Loops

Loops let you repeat tasks.

### For loop:
```cpp
for (int i = 0; i < 5; i++) {
    cout << "Number: " << i << endl;
}
```

### While loop:
```cpp
int i = 0;
while (i < 3) {
    cout << "i is " << i << endl;
    i++;
}
```

### Do-while loop:
```cpp
int j = 0;
do {
    cout << "j is " << j << endl;
    j++;
} while (j < 2);
```

Loops are used when you want to repeat something multiple times.
""",
        "lesson_order": 7
    },
    {
        "lesson_title": "Functions",
        "content": """
# Functions

Functions help you organize your code.

```cpp
void greet(string name) {
    cout << "Hello, " << name << "!" << endl;
}

int main() {
    greet("Alice");
    greet("Bob");
    return 0;
}
```

### Explanation:
- `void greet(string name)` defines a function
- You can call it with different values

Functions are great for reusing logic.
""",
        "lesson_order": 8
    },
    {
        "lesson_title": "Arrays",
        "content": """
# Arrays

Arrays store multiple values of the same type.

```cpp
int numbers[4] = {10, 20, 30, 40};

for (int i = 0; i < 4; i++) {
    cout << numbers[i] << endl;
}
```

### Explanation:
- `int numbers[4]` creates an array with 4 integers
- You can access each element using an index like `numbers[0]`

Arrays are helpful for managing groups of similar data.
""",
        "lesson_order": 9
    },
    {
        "lesson_title": "Classes and Objects",
        "content": """
# Classes and Objects

C++ supports object-oriented programming.

```cpp
class Car {
public:
    string brand;
    int year;

    void honk() {
        cout << "Beep!" << endl;
    }
};

int main() {
    Car myCar;
    myCar.brand = "Toyota";
    myCar.year = 2020;
    myCar.honk();
    cout << myCar.brand << " - " << myCar.year << endl;
    return 0;
}
```

### Explanation:
- `class Car` defines a blueprint
- We create an object `myCar` from that class
- We access and use its members
""",
        "lesson_order": 10
    },
    {
        "lesson_title": "Final Project: Simple Student Record",
        "content": """
# Final Project: Simple Student Record

Let’s build a tiny system to store student info.

```cpp
class Student {
public:
    string name;
    int age;

    void display() {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
    }
};

int main() {
    Student s1;
    s1.name = "Luna";
    s1.age = 18;
    s1.display();
    return 0;
}
```

### Explanation:
- We defined a `Student` class with properties and a method
- We created a student and printed the info

🎉 You just finished your first C++ project!
""",
        "lesson_order": 11
    }
]

for lesson in lessons:
    lesson_id = str(uuid.uuid4())
    cursor.execute(
        """
INSERT INTO Lesson (lesson_id, course_id, lesson_title, content, lesson_order) VALUES (?, ?, ?, ?, ?)
""",
        (
            lesson_id,
            cplusplus_course_id ,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
