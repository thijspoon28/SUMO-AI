from core.exceptions.base import CustomException


class MatchNotFoundException(CustomException):
    status_code = 404
    error_code = "MATCH__NOT_FOUND"
    message = "match not found"
