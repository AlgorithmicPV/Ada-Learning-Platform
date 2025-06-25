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

import sqlite3

conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()

# cursor.execute("SELECT lesson_id FROM user_lesson WHERE status ='completed' ")

# completed_lessons_id = cursor.fetchall()

# lesson_ids = []

# for tuple_item in completed_lessons_id:
#     for uuid in tuple_item:
#         lesson_ids.append(uuid)



# if "03e1fcbe-406b-4494-b5as7-a4f7d0b935ae" not in lesson_ids:
#     print("fine")

cursor.execute("SELECT course_id FROM Course")

course_id_tuple = cursor.fetchall()

course_ids = []

for element in course_id_tuple:
    for course_id in element:
        course_ids.append(course_id)

print(course_ids)