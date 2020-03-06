from email_validator import validate_email


def lc_validate_email(email):
    # assume this may be executed behind internal corp proxy
    validate_email(email, check_deliverability=False)
    return email
