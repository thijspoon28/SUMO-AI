from core.exceptions.base import CustomException


class RikishiNotFoundException(CustomException):
    status_code = 404
    error_code = "RIKISHI__NOT_FOUND"
    message = "rikishi not found"
