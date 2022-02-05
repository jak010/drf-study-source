import sys

from rest_framework.views import exception_handler
from rest_framework.views import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied

from rest_framework.serializers import as_serializer_error
from django.db.utils import DataError as _DataBaseError


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class DataBaseError(_DataBaseError):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


def custom_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, context)

    if response is None:
        data = {'message': '', 'extra': ''}

        if isinstance(exc, ApplicationError):  # API Level
            data['message'] = exc.message
            data['extra'] = exc.extra
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if isinstance(exc, AttributeError):
            data['message'] = exc.args
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc.detail, (list, dict)):  # Exception Level
        response.data = {
            'detail': response.data
        }

    if isinstance(exc, exceptions.ValidationError):  # Validation Level
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data['detail']

    return response
