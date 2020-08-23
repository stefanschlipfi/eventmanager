from rest_framework.exceptions import APIException
from rest_framework import status

class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

class MethodNotAllowedException(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = "This HTTP Method is not allowed"
    default_code = "HTTP_ERROR"

class ObjectExistsException(APIException):
    status_code =  status.HTTP_409_CONFLICT
    default_detail = "Object allready exits"
    default_code = "Database_ERROR"