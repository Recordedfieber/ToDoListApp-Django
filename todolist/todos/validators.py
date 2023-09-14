from django.core.exceptions import ValidationError
from django.core import validators


class PriorityValidator(validators.RegexValidator):
    regex = r'^#\d+$'
    message = "Priority must start with '#' and contain only numeric characters after that."
    flags = 0
