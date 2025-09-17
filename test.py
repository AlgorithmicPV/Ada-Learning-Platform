
def check_characters_limit(max_length: int, input: str):
    cleaned_input = input.strip()

    input_length = len(cleaned_input)

    if max_length < input_length:
        return "reject"
    return "accept"


print(check_characters_limit(2, "  HI  "))
