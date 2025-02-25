from core.exceptions.base import CustomException


class BashoNotFoundException(CustomException):
    status_code = 404
    error_code = "BASHO__NOT_FOUND"
    message = "basho not found"
