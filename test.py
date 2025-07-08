import string
translator = str.maketrans('', '', string.punctuation)

questions = [
    "How do I create a login page in Flask?",
    "What is the difference between GET and POST methods?",
    "How can I deploy a Flask app to Heroku?",
    "What is the purpose of virtual environments in Python?",
    "How to connect a Flask app with a SQLite database?",
    "Why is my Flask route not working?",
    "How do I implement user authentication in Flask?",
    "What are Flask blueprints and how do they work?",
    "How can I hash passwords securely in Flask?",
    "How to create a search bar using Flask and JavaScript?",
    "How do I pass data from HTML form to Flask backend?",
    "What is the best way to organize a Flask project?",
    "How do I handle 404 errors in Flask?",
    "How to validate form inputs in Flask using WTForms?",
    "Can I use sessions to store user data in Flask?",
    "How to display flash messages in Flask templates?",
    "How do I render dynamic content with Jinja2?",
    "What is the difference between Flask and Django?",
    "How to make an API with Flask and return JSON?",
    "How to include static files like CSS in a Flask project?"
]


def clean_the_text(text):
    clean_text = text.translate(translator).lower()
    return clean_text


input = "How do I send data to the flask backend from html"


one_question = questions[10]


input_array = clean_the_text(input).split(" ")
input_array = list(set(input_array))

one_question_array = clean_the_text(one_question).split(" ")
one_question_array = list(set(one_question_array))


if len(one_question_array) < len(input_array):
    down_number = len(one_question_array)
else:
    down_number = len(input_array)

input_set = set(input_array)
one_question_set = set(one_question_array)

common_words = len(one_question_set.intersection(input_set))

percentage_of_equility = (common_words/down_number)*100
print(percentage_of_equility)

if percentage_of_equility >= 50:
    print("same idea")
