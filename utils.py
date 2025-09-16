import sqlite3
from functools import wraps
from email_validator import validate_email, EmailNotValidError
from flask import redirect, session, url_for, request


# Function to divide an array into chunks of a specified size
# This is used to display the courses in a grid format on the frontend
def divide_array_into_chunks(
    dividing_array, chunk_size
):  # Divides an array into chunks of a specified size
    new_array = []
    for i in range(
        int(
            (len(dividing_array)) / (chunk_size)
        )
        # Calculates the number of chunks needed by
        # dividing the length of the array
        # by the chunk size and
        # converting it to an integer as it is a float value
    ):  # Iterates over the array in chunks
        new_array.append(
            dividing_array[
                (chunk_size * i): (chunk_size + (chunk_size * i))
                # {chunk_size * i} is the starting index of the chunk,
                # and {chunk_size + (chunk_size * i)}
                # is the ending index of the chunk
            ]
        )  # Appends the chunk to the new array,
    return new_array


def validate_email_address(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        if email_info:
            return "valid"
        else:
            return "invalid"
    except EmailNotValidError:
        return "invalid"


def db_execute(
        *,
        query: str,
        fetch: bool = False,
        fetchone: bool = False,
        values: tuple | list | dict | None = None,
):
    try:
        conn = sqlite3.connect("database/app.db")
        cursor = conn.cursor()
        cursor.execute(query, values)
        if fetch:
            if fetchone:
                return cursor.fetchone()
            else:
                return cursor.fetchall()
        else:
            conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)
        return None


# Why @wraps matters:
# - Without @wraps:
#       Flask registers the wrapped function under the name "wrapper"
#       Then url_for("<bp>.test") fails
#       because the endpoint is "wrapper", not "test"
# - With @wraps(view_func):
#       The wrapper keeps the original function’s identity
#       (name/module/doc), so the endpoint stays "test" and url_for(...) works.
def login_required(endpoint_func):
    @wraps(endpoint_func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            return endpoint_func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login", next=request.full_path))
    return wrapper
