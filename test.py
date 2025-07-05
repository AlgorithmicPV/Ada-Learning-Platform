# # course_id = "7da7fd5f-8ff3-4ef7-9431-20c42961f16e"

# # cursor.execute(
# #     "SELECT lesson_id, lesson_title FROM Lesson WHERE course_id = ?", (course_id,)
# # )
# # lessons_rows = cursor.fetchall()

# # print(len(lessons_rows))

# # # for lesson_row in lessons_rows:
# # #     print(lesson_row[1])

# import sqlite3

# conn = sqlite3.connect("database/app.db")
# cursor = conn.cursor()

# # cursor.execute("SELECT lesson_id FROM user_lesson WHERE status ='completed' ")

# # completed_lessons_id = cursor.fetchall()

# # lesson_ids = []

# # for tuple_item in completed_lessons_id:
# #     for uuid in tuple_item:
# #         lesson_ids.append(uuid)


# # if "03e1fcbe-406b-4494-b5as7-a4f7d0b935ae" not in lesson_ids:
# #     print("fine")

# cursor.execute("SELECT course_id FROM Course")

# course_id_tuple = cursor.fetchall()

# course_ids = []

# completed_course_ids = []

# for element in course_id_tuple:
#     for course_id in element:
#         cursor.execute("""SELECT COUNT(*) FROM Lesson WHERE course_id=?""", (course_id,))


#         total_number_of_lessons = cursor.fetchone()[0]

#         # print(total_number_of_lessons)

#         cursor.execute("""SELECT COUNT(*) FROM user_lesson WHERE lesson_id IN (SELECT lesson_id FROM lesson WHERE course_id = ?) AND status = "completed" """, (course_id,))

#         number_completed_lesson = cursor.fetchone()[0]

#         # print(number_completed_lesson)

#         if number_completed_lesson == total_number_of_lessons:
#             completed_course_ids.append(course_id)

# # print(completed_course_ids)

# completed_courses_data = []

# for completed_course_id in completed_course_ids:
#     cursor.execute(
#             "SELECT course_id, course_name, language_image, course_image, language FROM Course WHERE course_id=?", (completed_course_id,)
#         )
#     course_data = cursor.fetchall()
#     for one_set_course_data in course_data:
#         for data in one_set_course_data:
#             completed_courses_data.append(data)
#         completed_courses_data.append(100)

# print(completed_courses_data)
#     # print(course_data)
#     # for data in course_data:
#     #     # completed_course_data = (data)
#     #     print(data)
#     # completed_course_data=  completed_course_data + (100,)


# # print(completed_course_data)

# # for i in completed_course_data:
# #     print(i[1])

# from openai import OpenAI
# from dotenv import load_dotenv
# import os


# load_dotenv()

# token = os.getenv("GITHUB_TOKEN")
# endpoint = "https://models.github.ai/inference"
# model = "openai/gpt-4.1"


# client = OpenAI(
#     base_url=endpoint,
#     api_key=token,
# )

# user_input = "Make me a course on React"

# response = client.chat.completions.create(
# messages=[
#         {
#             "role": "system",
#             "content": f"You are an AI assistant integrated into the Ada Learning Platform, developed by G. A. Pasindu Vidunitha. Your role is to generate a simple, clear, and suitable course name based on the following user input: {user_input}",
#         },
#         {
#             "role": "user",
#             "content": user_input,
#         },
#     ],
#     temperature=1,
#     top_p=1,
#     model=model,
#     )


# course_name =  response.choices[0].message.content

# print(course_name)

# response = client.chat.completions.create(
# messages=[
#         {
#             "role": "system",
#             "content": f"",
#         },
#         {
#             "role": "user",
#             "content": f"You are an AI assistant integrated into the Ada Learning Platform, developed by G. A. Pasindu Vidunitha. Ada is a platform built to help beginner developers learn programming and software development effectively. Your task is to generate beginner-friendly, easy-to-understand course content based on the following user input: {user_input}. Use HTML tags for all output—including headings, paragraphs, lists, code blocks, and inline comments—so the content can be directly rendered in a webpage. Do not include introductions, explanations, or phrases like “Here is your course.” Only output structured content using HTML."
#         },
#     ],
#     temperature=1,
#     top_p=1,
#     model=model,
#     )

# course_content = response.choices[0].message.content

# print(course_content)

# user_input = ""
# if not user_input.strip():
#     print("Input is empty.")
# else:
#     print("Input is not empty:", user_input)

# conn = sqlite3.connect("database/app.db")
# cursor = conn.cursor()

# cursor.execute("SELECT resource_id, title, status, generated_at FROM Ai_resource")

# ai_courses_data_form_db = cursor.fetchall()

# # print(ai_courses_data)

# ai_courses_data = []
# ai_course = []

# for ai_Course_from_db in ai_courses_data_form_db:
#     # ai_course.append(ai_Course_from_db[])
#     ai_course.append(ai_Course_from_db[1])
#     ai_course.append(ai_Course_from_db[])
#     ai_course.append(ai_Course_from_db[3].split("T")[0])

# print(ai_course)


# date = "2025-06-30T19:03:42"

# print(date.split("T")[0])

# ai_courses_data = [['f67149f9-c2b2-4e3c-a8fe-1fe84c2c3a7c', 'Introduction to Vue.js', "Haven't Done", '2025-06-30'], ['1ac0385e-699a-4c16-9d75-e739bc94b03f', 'Introduction to AngularJS', "Haven't Done", '2025-06-30'], ['e9542a54-c9f6-4c96-a70d-f887acfbd707', 'FastAPI Mastery', "Haven't Done", '2025-06-30'], ['a5f9b99b-d011-44dd-9045-23ab2b863910', 'Introduction to Web Development with Flask', "Haven't Done", '2025-06-30']]

# keyword = "FastApi"

# searched_ai_courses_data = []

# keyword = keyword.lower()
# for ai_course_data in ai_courses_data:
#     for data in ai_course_data:
#         data = data.lower()
#         if keyword in data:
#             searched_ai_courses_data.append(ai_course_data)
#             break

# print(searched_ai_courses_data)


# cursor.execute(
#     "SELECT title , content FROM Ai_resource WHERE resource_id = '875cc8a3-02e5-49df-b7c8-4e58c9775ab1'"
# )
# row = cursor.fetchall()[0]

# print(row[0])

import sqlite3
from datetime import datetime, date

conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()


cursor.execute("SELECT chat_id, user_id, question, created_at FROM Chat")
chat_details = cursor.fetchall()

date_sorted_chat_details = []

format_string = "%Y-%m-%dT%H:%M:%S"
for i in chat_details:
    raw_date = i[3]
    converted_date = datetime.strptime(raw_date, format_string)
    # print(type(converted_date))

    prev_date = converted_date
    # print(datetime.strptime(raw_date, format_string))


# chat_details.reverse()
# chat_cards_detail = []


# for chat_detail in chat_details:
#     user_id = chat_detail[1]
#     chat_id = chat_detail[0]

#     cursor.execute("SELECT full_name, profile_image FROM User WHERE user_id=?", (user_id,))
#     user_data = cursor.fetchall()[0]


#     cursor.execute("SELECT COUNT(*) FROM Reply WHERE chat_id = ?", (chat_id,))
#     number_of_replies = cursor.fetchone()

#     chat_detail += user_data
#     chat_detail += number_of_replies

#     temp_chat_detail = list(chat_detail)

#     today = date.today()
#     chat_date = (chat_detail[3].split("T")[0])
#     if str(today) == chat_date:
#         time_str = chat_detail[3].split("T")[1]
#         time_obj = datetime.strptime(time_str, '%H:%M:%S')
#         time_12hr = time_obj.strftime('%I:%M %p')
#         temp_chat_detail[3] = time_12hr
#     else:
#         temp_chat_detail[3] = chat_date

#     chat_detail = tuple(temp_chat_detail)

#     chat_cards_detail.append(chat_detail)

# print(chat_cards_detail)

# for test in chat_cards_detail:
#     # print(test)
#     for i in test:
#         print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
#         print(i)

# for i in chat_cards_detail:
#     print(i[3])


test = [5, 2, 9, 1, 3]

sorted_test = []

n = 0

# while not len(sorted_test) == len(test):
#     # sorted_test.append(test[n])
#     prev_data = 0
#     for i in range(len(test)):
#         if prev_date <
#     # n = n + 1

prev_date = 0
# for i in range(len(test)):
#     # prev_date = test[i]
#     for t in range(len(test)):
#         while prev_date < test[t]:
#             prev_date = test[t]
#         else:
#             prev_date = prev_date
#     sorted_test.append(test[t])
#     test.remove(test[t])


# for i in range(len(test)):
#     for t  in range(len(test)):
#         if (t + 1) < len(test):
#             next_data = test[t + 1]
#         else:
#             next_data = test[t]
#         if test[t] < next_data:
#             print(f"{t} is greater than {t + 1}")
#             temp_max = test[i]
#         else:
#             print(f"{t} is smaller than {t + 1}")


# print(sorted_test)


for i in range(len(test)):
    if (i + 1) < len(test):
        next_data = test[i + 1]
    else:
        next_data = test[i]
    while test[i] > prev_date:
        print(f"{test[i]} is the highest")
        break
