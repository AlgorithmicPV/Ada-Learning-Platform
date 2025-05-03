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

Hey there! 👋 Welcome to your TypeScript journey.

If you’ve already touched JavaScript (even just a little), you’ll love what TypeScript brings. It adds features like type safety, better autocompletion, and more confidence in your code.

### Why Learn TypeScript?
- It helps catch mistakes before running your code
- It makes your code easier to understand and maintain
- It's widely used in professional web development

Let’s take it step by step — no rush. Ready? Let's get started!
""",
        "lesson_order": 1
    },
    {
        "lesson_title": "Setting Up TypeScript",
        "content": """
# Setting Up TypeScript

Let’s get your computer ready to write TypeScript!

### Step 1: Install Node.js
If you don’t already have Node.js:
- Go to [https://nodejs.org](https://nodejs.org)
- Download and install the LTS version

### Step 2: Install TypeScript
Open your terminal and run:
```bash
npm install -g typescript
```
This makes the `tsc` command (TypeScript compiler) available globally.

### Step 3: Check it works
```bash
tsc --version
```
If you see a version number, you're good to go!

Next up: let’s write our first TypeScript program!
""",
        "lesson_order": 2
    },
    {
        "lesson_title": "Your First TypeScript Program",
        "content": """
# Your First TypeScript Program

Create a file named `hello.ts` and write this code:
```ts
let message: string = "Hello, TypeScript!";
console.log(message);
```

### What does this do?
- We declare a variable `message`
- `: string` tells TypeScript that `message` must always be a string
- We print it using `console.log()`

### Run it:
First, compile it:
```bash
tsc hello.ts
```
This creates `hello.js`

Now run it with Node:
```bash
node hello.js
```

🎉 You just ran your first TypeScript program!
""",
        "lesson_order": 3
    },
    {
        "lesson_title": "Variables and Types",
        "content": """
# Variables and Types

TypeScript makes JavaScript better by letting you specify types.

```ts
let name: string = "Alice";
let age: number = 30;
let isStudent: boolean = true;
```

### Explanation:
- `string`, `number`, and `boolean` are basic types
- If you try to assign a wrong type later, TypeScript will warn you

Example:
```ts
age = "thirty"; // ❌ Error: 'string' is not assignable to 'number'
```

This helps you catch bugs early!
""",
        "lesson_order": 4
    },
    {
        "lesson_title": "Functions with Types",
        "content": """
# Functions with Types

Let’s write a simple function in TypeScript.

```ts
function greet(name: string): void {
  console.log("Hello, " + name);
}

greet("Bob");
```

### What’s going on?
- `name: string` tells us the function needs a string
- `void` means it returns nothing

Let’s try a function that returns something:
```ts
function add(a: number, b: number): number {
  return a + b;
}

console.log(add(5, 3));
```

Adding types makes your code safer and easier to understand.
""",
        "lesson_order": 5
    },
    {
        "lesson_title": "Arrays and Tuples",
        "content": """
# Arrays and Tuples

Arrays hold lists of values.

```ts
let fruits: string[] = ["apple", "banana", "cherry"];
console.log(fruits[0]);
```

We specify what type of items are in the array (`string[]`).

### Tuples
Tuples are like arrays, but with fixed types and order.
```ts
let person: [string, number] = ["Alice", 30];
```

- First must be a string, second a number.
- Helps when position and type both matter.
""",
        "lesson_order": 6
    },
    {
        "lesson_title": "Objects and Interfaces",
        "content": """
# Objects and Interfaces

Let’s define a person using an object.

```ts
let person = {
  name: "Bob",
  age: 28
};
console.log(person.name);
```

### Adding structure with interfaces:
```ts
interface Person {
  name: string;
  age: number;
}

let student: Person = {
  name: "Alice",
  age: 20
};
```

Interfaces make sure the object has all required fields — and correct types.
""",
        "lesson_order": 7
    },
    {
        "lesson_title": "Union and Literal Types",
        "content": """
# Union and Literal Types

What if something could be more than one type?

### Union type:
```ts
let id: number | string;
id = 101;
id = "A102";
```

You can use `|` to allow multiple types.

### Literal type:
```ts
let direction: "left" | "right";
direction = "left"; // ✅
direction = "up";   // ❌ Error
```

Use these when you want exact values only.
""",
        "lesson_order": 8
    },
    {
        "lesson_title": "Type Aliases and Enums",
        "content": """
# Type Aliases and Enums

### Type Aliases
They let you create custom type names.
```ts
type ID = number | string;
let userId: ID = 123;
```

### Enums
Great for a fixed set of values.
```ts
enum Color {
  Red,
  Green,
  Blue
}

let myColor: Color = Color.Green;
console.log(myColor); // prints 1
```

Enums start at 0 by default.
""",
        "lesson_order": 9
    },
    {
        "lesson_title": "Type Assertions and Casting",
        "content": """
# Type Assertions and Casting

Sometimes, you know more than TypeScript. You can tell it:
```ts
let someValue: any = "this is a string";
let strLength: number = (someValue as string).length;
```

Or with angle brackets:
```ts
let len = (<string>someValue).length;
```

This is useful when working with external data.
""",
        "lesson_order": 10
    },
    {
        "lesson_title": "Classes and Inheritance",
        "content": """
# Classes and Inheritance

TypeScript supports OOP with classes.

```ts
class Animal {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
  move() {
    console.log(this.name + " moves.");
  }
}

class Dog extends Animal {
  bark() {
    console.log("Woof!");
  }
}

let dog = new Dog("Buddy");
dog.move();
dog.bark();
```

Use classes to structure and reuse your code.
""",
        "lesson_order": 11
    },
    {
        "lesson_title": "Your Final Project: A User Profile Form",
        "content": """
# Your Final Project: A User Profile Form

Let’s bring it all together into a small project.

```ts
interface User {
  name: string;
  age: number;
  isStudent: boolean;
}

function createUser(user: User): void {
  console.log("Welcome, " + user.name);
  if (user.isStudent) {
    console.log("You're a student!");
  }
}

let newUser: User = {
  name: "Alice",
  age: 22,
  isStudent: true
};

createUser(newUser);
```

### What we did:
- Used an interface
- Created and passed an object
- Printed a message based on values

🎉 You now know the basics of TypeScript. Great job!
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
            typescript_course_id,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
