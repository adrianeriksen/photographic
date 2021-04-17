from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class AlphanumericUsernameValidator(validators.RegexValidator):
    regex = r"^[a-zA-Z0-9]+\Z"
    message = (
        "Enter a valid username. This value may contain only English letters, ",
        "and numbers.",
    )
    flags = 0
