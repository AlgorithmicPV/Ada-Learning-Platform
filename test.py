from email_validator import validate_email, EmailNotValidError

email = "my+address@examplm"


def validate_email_address(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        print("valid")
    except EmailNotValidError as e:
        print("invalid")


validate_email_address(email)
