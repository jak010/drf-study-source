from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateNameError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Duplicate Name"


class AlreadyExistPerson(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "AlreadyExistPerson"
