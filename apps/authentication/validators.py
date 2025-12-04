from rest_framework.fields import RegexValidator



PHONE_VALIDATOR = RegexValidator(
    regex=r'^09[0-9]{9}$',
    message="Phone number must be exactly 11 digits starting with 09"
)