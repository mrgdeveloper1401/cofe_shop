from rest_framework import exceptions, views


class PasswordNotMatch(exceptions.APIException):
    default_detail = "پسورد قبلی شما اشتباه وارد شده هست"


class PasswordNotEqaul(exceptions.APIException):
    default_detail = "پسورد جدید شما با هم برابر نیست"
    status_code = 400
    default_code = "PASSWORD_NOT_EQAUL"


class UserNotFound(exceptions.APIException):
    status_code = 404
    default_detail = "کاربر یافت نشد"
    default_code = "USER_NOT_FOUND"


class UserNotActive(exceptions.APIException):
    status_code = 403
    default_detail = "حساب شما مسدود میباشد"
    default_code = "USER_INACTIVE"


class OtpNotFound(exceptions.APIException):
    status_code = 404
    default_detail = "کد پیدا نشد"
    default_code = "CODE_NOT_FOUND"


def custom_exception_handler(exc, context):
    response = views.exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            "success": False,
            "message": response.data.get("detail", "خطای ناشناخته"),
            "status_code": response.status_code
        }

    return response
