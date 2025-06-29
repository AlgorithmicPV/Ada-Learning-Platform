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

completed_course_ids = []

for element in course_id_tuple:
    for course_id in element:
        cursor.execute("""SELECT COUNT(*) FROM Lesson WHERE course_id=?""", (course_id,))

        
        total_number_of_lessons = cursor.fetchone()[0]

        # print(total_number_of_lessons)

        cursor.execute("""SELECT COUNT(*) FROM user_lesson WHERE lesson_id IN (SELECT lesson_id FROM lesson WHERE course_id = ?) AND status = "completed" """, (course_id,))

        number_completed_lesson = cursor.fetchone()[0]

        # print(number_completed_lesson)

        if number_completed_lesson == total_number_of_lessons:
            completed_course_ids.append(course_id)

# print(completed_course_ids)

completed_courses_data = []

for completed_course_id in completed_course_ids:
    cursor.execute(
            "SELECT course_id, course_name, language_image, course_image, language FROM Course WHERE course_id=?", (completed_course_id,)
        )
    course_data = cursor.fetchall()
    for one_set_course_data in course_data:
        for data in one_set_course_data:
            completed_courses_data.append(data)
        completed_courses_data.append(100)

print(completed_courses_data)
    # print(course_data)
    # for data in course_data:
    #     # completed_course_data = (data)
    #     print(data)
    # completed_course_data=  completed_course_data + (100,) 
        


# print(completed_course_data)

# for i in completed_course_data:
#     print(i[1])