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
        "lesson_title": "Welcome to TypeScript",
        "content": """
# Welcome to TypeScript

TypeScript is a language that builds on JavaScript by adding **static types**. It helps catch errors early and makes your code easier to understand and maintain.

### Why Learn TypeScript?
- Type safety: Catch mistakes at compile time
- Great for beginners transitioning to serious development
- Used in large projects like Angular, Microsoft tools, and many startups

This course assumes **no prior experience** with JavaScript or TypeScript.
""",
        "lesson_order": 1
    },
    {
        "lesson_title": "Setting Up TypeScript",
        "content": """
# Setting Up TypeScript

### Option 1: Online Playground
Go to [TypeScript Playground](https://www.typescriptlang.org/play) — no installation needed.

### Option 2: Local Setup
1. Install Node.js from [https://nodejs.org](https://nodejs.org)
2. Open terminal:
```bash
npm install -g typescript
```
3. Create file:
```bash
tsc --init
```
Now you're ready to write `.ts` files.
""",
        "lesson_order": 2
    },
    {
        "lesson_title": "Hello TypeScript",
        "content": """
# Hello TypeScript

Create a file called `hello.ts` and add:
```typescript
let message: string = "Hello, TypeScript!";
console.log(message);
```

Compile and run:
```bash
tsc hello.ts
node hello.js
```
You should see: `Hello, TypeScript!`
""",
        "lesson_order": 3
    },
    {
        "lesson_title": "Variables and Types",
        "content": """
# Variables and Types

TypeScript allows you to **declare variables with types**:
```typescript
let name: string = "Alice";
let age: number = 30;
let isStudent: boolean = true;
```

### Type Inference
You can omit the type if it's obvious:
```typescript
let country = "New Zealand"; // inferred as string
```
""",
        "lesson_order": 4
    },
    {
        "lesson_title": "Basic Input and Output",
        "content": """
# Basic Input and Output

In TypeScript, you use `console.log()` for output.
```typescript
console.log("Hello from TypeScript");
```

Input from the user requires additional setup like readline:
```typescript
import * as readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question("What is your name? ", function(name) {
  console.log("Hello, " + name);
  rl.close();
});
```
""",
        "lesson_order": 5
    },
    {
        "lesson_title": "Operators and Expressions",
        "content": """
# Operators and Expressions

### Arithmetic:
```typescript
let a = 10;
let b = 3;
console.log(a + b);
```

### Comparison:
```typescript
console.log(a > b);
console.log(a === 10);
```

### Logical:
```typescript
console.log(true && false);
```
""",
        "lesson_order": 6
    },
    {
        "lesson_title": "Conditionals (if/else)",
        "content": """
# Conditionals (if/else)

```typescript
let score = 85;

if (score >= 90) {
  console.log("A");
} else if (score >= 75) {
  console.log("B");
} else {
  console.log("C");
}
```
""",
        "lesson_order": 7
    },
    {
        "lesson_title": "Loops (for and while)",
        "content": """
# Loops (for and while)

### for loop:
```typescript
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

### while loop:
```typescript
let count = 0;
while (count < 5) {
  console.log(count);
  count++;
}
```
""",
        "lesson_order": 8
    },
    {
        "lesson_title": "Functions",
        "content": """
# Functions

```typescript
function greet(name: string): void {
  console.log("Hello, " + name);
}

greet("Alice");

function add(x: number, y: number): number {
  return x + y;
}

console.log(add(2, 3));
```
""",
        "lesson_order": 9
    },
    {
        "lesson_title": "Arrays and Tuples",
        "content": """
# Arrays and Tuples

### Arrays:
```typescript
let numbers: number[] = [1, 2, 3];
console.log(numbers[0]);
```

### Tuples:
```typescript
let person: [string, number] = ["Alice", 25];
console.log(person[1]);
```
""",
        "lesson_order": 10
    },
    {
        "lesson_title": "Interfaces and Objects",
        "content": """
# Interfaces and Objects

### Object:
```typescript
let user = {
  name: "Alice",
  age: 30
};
console.log(user.name);
```

### Interface:
```typescript
interface Person {
  name: string;
  age: number;
}

let employee: Person = { name: "Bob", age: 40 };
console.log(employee.age);
```
""",
        "lesson_order": 11
    },
    {
        "lesson_title": "Error Handling",
        "content": """
# Error Handling

```typescript
try {
  throw new Error("Something went wrong");
} catch (e) {
  console.log("Caught error:", e.message);
}
```
""",
        "lesson_order": 12
    },
    {
        "lesson_title": "Classes and OOP Basics",
        "content": """
# Classes and OOP Basics

```typescript
class Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  speak(): void {
    console.log(this.name + " makes a sound");
  }
}

let dog = new Animal("Dog");
dog.speak();
```
""",
        "lesson_order": 13
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
            typescript_course_id,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
