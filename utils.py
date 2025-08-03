from email_validator import validate_email, EmailNotValidError
import sqlite3

# Function to divide an array into chunks of a specified size
# This is used to display the courses in a grid format on the frontend


def divide_array_into_chunks(
    dividing_array, chunk_size
):  # Divides an array into chunks of a specified size
    new_array = []
    for i in range(
        int(
            (len(dividing_array)) / (chunk_size)
        )  # Calculates the number of chunks needed by dividing the length of the array by the chunk size and converting it to an integer as it is a float value
    ):  # Iterates over the array in chunks
        new_array.append(
            dividing_array[
                (chunk_size * i): (chunk_size + (chunk_size * i))
                # {chunk_size * i} is the starting index of the chunk, and {chunk_size + (chunk_size * i)} is the ending index of the chunk
            ]
        )  # Appends the chunk to the new array,
    return new_array


def validate_email_address(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return "valid"
    except EmailNotValidError as e:
        return "invalid"

# Uses a function to reduce repetition when connecting to the database
# No need to call conn.close() manually — it's automatically handled when using 'with'
# Still need to use cursor = conn.cursor() because some routes run multiple SQL queries
# If I wrapped everything in one function, I'd have to call it multiple
# times per route, which would affect performance


def get_connection():
    return sqlite3.connect("database/app.db")
