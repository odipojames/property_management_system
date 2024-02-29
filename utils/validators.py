import re
from django.core.exceptions import ValidationError



def validate_international_phone_number(phone):
    """
    Validate an international phone number.
    - Number must have country code, ie +254, etc
    - Number must contain no spaces
    - Number must be of correct length
    - Number must have no letters

    https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers

    return True if number is valid. False otherwise.
    """

    regex_pattern = r"^\+(?:[0-9]●?){6,14}[0-9]$"

    match = re.search(regex_pattern, phone)

    if not match:
        raise ValidationError(["please enter correct international phone number."])
    return phone