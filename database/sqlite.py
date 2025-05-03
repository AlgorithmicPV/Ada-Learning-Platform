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
        "lesson_title": "Welcome to Java Programming",
        "content": """
# Welcome to Java Programming

Hey there! 👋 Ready to start learning Java?

Java is one of the most widely-used programming languages in the world. From Android apps to enterprise systems, Java is everywhere!

### Why learn Java?
- It's beginner-friendly and strongly typed
- It's used in mobile apps, web apps, and backend services
- It's a great language for building solid programming foundations

We’ll start from the very basics, and by the end of this course, you’ll be writing real Java programs.

Let’s begin!
""",
        "lesson_order": 1
    },
    {
        "lesson_title": "Setting Up Java",
        "content": """
# Setting Up Java

Before writing Java code, we need to get Java installed.

### Step 1: Install Java
- Visit [https://www.oracle.com/java/technologies/javase-downloads.html](https://www.oracle.com/java/technologies/javase-downloads.html)
- Download and install the Java Development Kit (JDK)

### Step 2: Install an IDE (Optional, but helpful)
You can write Java using any text editor, but using an IDE like:
- IntelliJ IDEA (recommended)
- Eclipse
- VS Code (with Java extensions)

### Step 3: Verify Java Installation
Open your terminal and type:
```bash
java -version
javac -version
```

### Explanation:
- `java -version` checks if the Java runtime is installed
- `javac -version` checks if the Java compiler is installed

If both commands show a version number, you're all set!
""",
        "lesson_order": 2
    },
    {
        "lesson_title": "Your First Java Program",
        "content": """
# Your First Java Program

Let’s write a simple program that says "Hello, world!"

Create a file called `HelloWorld.java` with this code:
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
```

### Explanation:
- `public class HelloWorld` defines a class called HelloWorld
- `public static void main(String[] args)` is the method that Java runs first
- `System.out.println(...)` prints a message to the screen

### How to run:
1. Open your terminal and navigate to the file location
2. Compile the code:
```bash
javac HelloWorld.java
```
3. Then run it:
```bash
java HelloWorld
```

🎉 You should see: `Hello, world!`
""",
        "lesson_order": 3
    },
    {
        "lesson_title": "Variables and Data Types",
        "content": """
# Variables and Data Types

Java requires you to declare what type of data each variable holds.

```java
String name = "Alice";
int age = 25;
double height = 5.6;
boolean isStudent = true;
```

### Explanation:
- `String` holds text
- `int` is for whole numbers
- `double` is for decimal numbers
- `boolean` is for true/false values

To print them:
```java
System.out.println(name);
System.out.println(age);
```

This helps Java know what kind of data to expect and catch errors early.
""",
        "lesson_order": 4
    },
    {
        "lesson_title": "Taking Input from the User",
        "content": """
# Taking Input from the User

Use the `Scanner` class to read user input.

```java
import java.util.Scanner;

public class InputExample {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Enter your age: ");
        int age = scanner.nextInt();

        System.out.println("Hello, " + name + ". You are " + age + " years old.");
    }
}
```

### Explanation:
- `import java.util.Scanner;` brings in the Scanner class from Java's utility library
- `Scanner scanner = new Scanner(System.in);` sets up input reading from the keyboard
- `scanner.nextLine()` reads a line of text
- `scanner.nextInt()` reads a number
- We then print out a personalized greeting

This makes your programs interactive!
""",
        "lesson_order": 5
    },
    {
        "lesson_title": "If Statements",
        "content": """
# If Statements

Let's teach our program to make decisions.

```java
int age = 20;

if (age >= 18) {
    System.out.println("You are an adult.");
} else {
    System.out.println("You are a minor.");
}
```

### Explanation:
- `if (age >= 18)` checks whether the condition is true
- If it is, the first message is printed
- Otherwise, the `else` part runs

More conditions:
```java
if (age >= 65) {
    System.out.println("You are a senior.");
} else if (age >= 18) {
    System.out.println("You are an adult.");
} else {
    System.out.println("You are a minor.");
}
```

Use if/else to control what your program does based on values.
""",
        "lesson_order": 6
    },
    {
        "lesson_title": "Loops in Java",
        "content": """
# Loops in Java

Loops let you repeat code multiple times.

### For loop:
```java
for (int i = 0; i < 5; i++) {
    System.out.println("Count: " + i);
}
```

### Explanation:
- `int i = 0` sets the starting point
- `i < 5` is the condition to keep looping
- `i++` increases `i` by 1 each time
- The loop runs 5 times, printing 0 to 4

### While loop:
```java
int count = 0;
while (count < 3) {
    System.out.println("While count: " + count);
    count++;
}
```

This keeps looping as long as the condition is true.
""",
        "lesson_order": 7
    },
    {
        "lesson_title": "Methods (Functions)",
        "content": """
# Methods (Functions)

Methods help you organize code into reusable blocks.

```java
public class Greeter {
    public static void greet(String name) {
        System.out.println("Hello, " + name);
    }

    public static void main(String[] args) {
        greet("Alice");
        greet("Bob");
    }
}
```

### Explanation:
- `public static void greet(String name)` defines a method that takes a name
- You call it with different values to reuse the logic
- The `main` method runs when the program starts
""",
        "lesson_order": 8
    },
    {
        "lesson_title": "Arrays",
        "content": """
# Arrays

Arrays store multiple values of the same type.

```java
int[] numbers = {1, 2, 3, 4};
System.out.println(numbers[0]);
```

### Explanation:
- `int[]` declares an array of integers
- `{1, 2, 3, 4}` are the values stored
- `numbers[0]` accesses the first item

You can loop through arrays:
```java
for (int num : numbers) {
    System.out.println(num);
}
```

Use arrays to manage lists of values.
""",
        "lesson_order": 9
    },
    {
        "lesson_title": "Object-Oriented Basics",
        "content": """
# Object-Oriented Basics

Java is an object-oriented language — you define classes and create objects from them.

```java
class Person {
    String name;
    int age;

    void sayHello() {
        System.out.println("Hi, I'm " + name);
    }
}

public class Main {
    public static void main(String[] args) {
        Person p = new Person();
        p.name = "Alice";
        p.age = 30;
        p.sayHello();
    }
}
```

### Explanation:
- `class Person` defines a blueprint
- `name` and `age` are properties
- `sayHello()` is a method
- We create a `Person` object and call its method
""",
        "lesson_order": 10
    },
    {
        "lesson_title": "Exception Handling",
        "content": """
# Exception Handling

Use `try` and `catch` to deal with errors.

```java
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("You can't divide by zero!");
}
```

### Explanation:
- Code in `try` runs first
- If an error happens, it jumps to `catch`
- This stops the program from crashing and lets you handle it
""",
        "lesson_order": 11
    },
    {
        "lesson_title": "Final Project: Contact Book",
        "content": """
# Final Project: Contact Book

Let’s bring together what you've learned.

```java
class Contact {
    String name;
    String phone;

    void display() {
        System.out.println("Name: " + name);
        System.out.println("Phone: " + phone);
    }
}

public class ContactBook {
    public static void main(String[] args) {
        Contact c1 = new Contact();
        c1.name = "Alice";
        c1.phone = "123-456-7890";
        c1.display();
    }
}
```

### Explanation:
- We created a `Contact` class
- We added properties and a method to display them
- Then we made a `ContactBook` class to create and show a contact

🎉 You just finished your first Java mini project!
""",
        "lesson_order": 12
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
            java_course_id,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
