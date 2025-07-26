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
