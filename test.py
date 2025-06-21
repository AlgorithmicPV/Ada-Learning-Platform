# data = [
#     1,
#     "Course A",
#     "img/course_a1.png",
#     "img/course_a2.png",
#     "English",
#     75,
#     2,
#     "Course B",
#     "img/course_b1.png",
#     "img/course_b2.png",
#     "Spanish",
#     40,
#     3,
#     "Course C",
#     "img/course_c1.png",
#     "img/course_c2.png",
#     "French",
#     90,
#     4,
#     "Course D",
#     "img/course_d1.png",
#     "img/course_d2.png",
#     "German",
#     60,
#     5,
#     "Course E",
#     "img/course_e1.png",
#     "img/course_e2.png",
#     "Japanese",
#     25,
# ]


# def divide_array_into_chunks(
#     dividing_array, chunk_size
# ):  # Divides an array into chunks of a specified size
#     new_array = []
#     for i in range(
#         int((len(dividing_array)) / (chunk_size))
#     ):  # Iterates over the array in chunks
#         new_array.append(
#             dividing_array[(chunk_size * i) : (chunk_size + (chunk_size * i))]
#         )  # Appends the chunk to the new array,
#     return new_array


# test = divide_array_into_chunks(data, 6)

# print(test)


all_course = [
    [1, "Course A", "img/course_a1.png", "img/course_a2.png", "English", 75],
    [2, "Course B", "img/course_b1.png", "img/course_b2.png", "Spanish", 40],
    [3, "Course C", "img/course_c1.png", "img/course_c2.png", "French", 90],
    [4, "Course D", "img/course_d1.png", "img/course_d2.png", "German", 60],
    [5, "Course E", "img/course_e1.png", "img/course_e2.png", "Japanese", 25],
]


search_key = input("search: ").lower()


test_two = []

for course_block in all_course:
    for word in course_block:
        word = str(word).lower()
        if search_key in word:
            print(course_block)
            # test_two.append(course_block)

print(test_two)
