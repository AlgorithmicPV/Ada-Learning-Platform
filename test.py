# import sqlite3

# conn = sqlite3.connect("database/app.db")
# cursor = conn.cursor()

# course_id = "7da7fd5f-8ff3-4ef7-9431-20c42961f16e"

# cursor.execute(
#     "SELECT lesson_id, lesson_title FROM Lesson WHERE course_id = ?", (course_id,)
# )
# lessons_rows = cursor.fetchall()

# print(len(lessons_rows))

# # for lesson_row in lessons_rows:
# #     print(lesson_row[1])

import markdown

test = """
# Setting Up Python Before we start coding, we need to make sure Python is installed. ### Step 1: Install Python 1. Go to [https://www.python.org/downloads](https://www.python.org/downloads) 2. Download the latest version for your computer 3. During installation, make sure you tick the box that says **“Add Python to PATH”** ### Step 2: Try it out! Open your terminal (or command prompt) and type: ```bash python --version ``` You should see something like `Python 3.11.2` — that means it’s working! ### Optional: Use an Editor You can write code in: - **VS Code** (recommended) - **Thonny** (super beginner-friendly) - Or even just Notepad for now! You’re ready! Let’s write your first program.
"""

ouput = markdown.markdown(test)

print(ouput)