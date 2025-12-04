from rest_framework.exceptions import APIException


class PasswordNotMatch(APIException):
    default_detail = "پسورد قبلی شما اشتباه وارد شده هست"


class PasswordNotEqaul(APIException):
    default_detail = "پسورد جدید شما با هم برابر نیست"
