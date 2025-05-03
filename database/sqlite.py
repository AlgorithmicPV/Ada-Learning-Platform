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
        "lesson_title": "Welcome to JavaScript Programming",
        "content": """
# Welcome to JavaScript Programming

Hey there! 👋 Welcome to your first steps into JavaScript.

JavaScript is the language of the web. You’ll find it in websites, apps, and games — basically anything interactive on the internet.

### Why learn JavaScript?
- It’s one of the most popular programming languages
- Runs in every modern web browser
- Lets you build interactive websites and apps

Don’t worry if you’ve never coded before. This course will guide you step-by-step, like a friendly tutor. Let's dive in!
""",
        "lesson_order": 1
    },
    {
        "lesson_title": "How to Run JavaScript",
        "content": """
# How to Run JavaScript

Before we can write JavaScript, we need a place to run it. Luckily, you already have it — right inside your browser!

### Method 1: Using the Browser Console
This is great for quick experiments.

1. Open Chrome, Firefox, or Edge
2. Right-click anywhere on a webpage
3. Choose **Inspect** > then go to the **Console** tab

Now try typing this in:
```javascript
console.log("Hello from the console!");
```

### What happened?
- `console.log(...)` tells the browser to print something to the console
- The text you wrote (in quotes) shows up as a message

You just ran your first line of JavaScript!

### Method 2: Embedding JavaScript in HTML
Let’s write a tiny web page that runs JavaScript.

Create a file called `index.html` with this content:
```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First JS Page</title>
  </head>
  <body>
    <h1>Hello, HTML and JS!</h1>
    <script>
      console.log("Hello from inside the HTML!");
    </script>
  </body>
</html>
```

### What’s going on here?
- The `<script>` tag tells the browser: “Here comes some JavaScript”
- Anything inside it will run when the page loads
- `console.log(...)` works the same way here — it just prints to the console

Open the file in your browser, go to the console, and see the message. 🎉

That’s it! You’re now ready to start coding in JavaScript.
""",
        "lesson_order": 2
    },
    {
        "lesson_title": "Variables and Data Types",
        "content": """
# Variables and Data Types

Variables let us store values — like text, numbers, or true/false answers.

```javascript
let name = "Alice";
let age = 25;
let isStudent = true;
```

### Let’s explain:
- `let name = "Alice";` stores the text "Alice" in a variable called `name`
- `let age = 25;` stores the number 25
- `let isStudent = true;` stores a boolean value (true or false)

Try this:
```javascript
console.log(name);
console.log(age + 5);
```

JavaScript also supports `const` for values that don’t change, and `var` (older style).
""",
        "lesson_order": 3
    },
    {
        "lesson_title": "Working with Strings and Numbers",
        "content": """
# Working with Strings and Numbers

Strings are bits of text. Numbers are… numbers! Let’s use both.

```javascript
let message = "Hello, " + "world!";
let length = message.length;
let upper = message.toUpperCase();
```

### What does this do?
- The `+` joins (concatenates) two strings
- `.length` gives the number of characters
- `.toUpperCase()` makes it ALL CAPS

With numbers:
```javascript
let price = 20;
let quantity = 3;
let total = price * quantity;
console.log("Total:", total);
```

You can add, subtract, multiply, divide — just like in math.
""",
        "lesson_order": 4
    },
    {
        "lesson_title": "Getting User Input",
        "content": """
# Getting User Input

In the browser, we can use `prompt()` to ask the user for input.

```javascript
let name = prompt("What’s your name?");
console.log("Nice to meet you, " + name + "!");
```

### What happens:
- The browser shows a popup asking the user to type something
- The result is saved in the `name` variable
- Then we greet them in the console

Want to use numbers?
```javascript
let age = Number(prompt("How old are you?"));
console.log("Next year, you’ll be", age + 1);
```

We use `Number(...)` to convert the input from string to number.
""",
        "lesson_order": 5
    },
    {
        "lesson_title": "If Statements",
        "content": """
# If Statements

If statements help your program make decisions.

```javascript
let age = Number(prompt("How old are you?"));

if (age >= 18) {
  console.log("You’re an adult.");
} else {
  console.log("You’re not an adult yet.");
}
```

You can also add more conditions:
```javascript
if (age >= 65) {
  console.log("You’re a senior.");
} else if (age >= 18) {
  console.log("You’re an adult.");
} else {
  console.log("You’re a minor.");
}
```

JavaScript checks conditions in order — and runs the first one that is true.
""",
        "lesson_order": 6
    },
    {
        "lesson_title": "Loops (for and while)",
        "content": """
# Loops (for and while)

Loops help you repeat actions automatically.

### for loop:
```javascript
for (let i = 0; i < 5; i++) {
  console.log("Number:", i);
}
```

This runs 5 times — starting at 0 and stopping before 5.

### while loop:
```javascript
let count = 0;
while (count < 3) {
  console.log("Counting", count);
  count++;
}
```

`while` keeps going as long as the condition is true.
""",
        "lesson_order": 7
    },
    {
        "lesson_title": "Functions",
        "content": """
# Functions

Functions are reusable blocks of code.

```javascript
function greet(name) {
  console.log("Hello, " + name);
}

greet("Alice");
greet("Bob");
```

This function takes a `name` and prints a greeting.

You can also return values:
```javascript
function square(n) {
  return n * n;
}

console.log(square(4));
```

Functions help keep your code clean and organized.
""",
        "lesson_order": 8
    },
    {
        "lesson_title": "Arrays and Objects",
        "content": """
# Arrays and Objects

Arrays are lists of values:
```javascript
let fruits = ["apple", "banana", "orange"];
console.log(fruits[0]);
fruits.push("grape");
```

- Access items by index (starts at 0)
- `.push()` adds a new item to the end

Objects group data with names:
```javascript
let person = {
  name: "Alice",
  age: 25,
  isStudent: true
};

console.log(person.name);
```

Objects are like labeled boxes for data — very useful!
""",
        "lesson_order": 9
    },
    {
        "lesson_title": "Events and the DOM",
        "content": """
# Events and the DOM

JavaScript can make your web page interactive!

Create an HTML file:
```html
<button onclick="sayHello()">Click Me</button>
<script>
  function sayHello() {
    alert("Hello there!");
  }
</script>
```

Clicking the button runs the `sayHello()` function.

You can also access and change HTML:
```html
<p id="greeting"></p>
<button onclick="showGreeting()">Say Hi</button>
<script>
  function showGreeting() {
    document.getElementById("greeting").innerText = "Hi, friend!";
  }
</script>
```

This updates the content of the paragraph when clicked.
""",
        "lesson_order": 10
    },
    {
        "lesson_title": "Error Handling",
        "content": """
# Error Handling

Let’s keep our programs from crashing!

```javascript
try {
  let num = Number(prompt("Enter a number:"));
  console.log(10 / num);
} catch (error) {
  console.log("Something went wrong:", error);
}
```

You can also check for specific cases:
```javascript
if (isNaN(num)) {
  console.log("That’s not a number!");
}
```

Handling errors makes your code safer and friendlier.
""",
        "lesson_order": 11
    },
    {
        "lesson_title": "Your Final Project: A Simple Quiz Game",
        "content": """
# Your Final Project: A Simple Quiz Game

Let’s build a fun little game to test what you’ve learned!

```javascript
function startQuiz() {
  let score = 0;
  let answer1 = prompt("What’s 2 + 2?");
  if (Number(answer1) === 4) score++;

  let answer2 = prompt("What’s the capital of France?");
  if (answer2.toLowerCase() === "paris") score++;

  alert("You scored " + score + "/2!");
}

startQuiz();
```

You:
- Asked questions
- Took input
- Checked answers
- Showed a final score

🎉 You made a working JavaScript app! Keep building more!
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
            javascript_course_id,
            lesson["lesson_title"],
            lesson["content"],
            lesson["lesson_order"],
        ),
    )
    conn.commit()
print("done")
