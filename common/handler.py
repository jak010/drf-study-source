from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
from rest_framework.validators import UniqueValidator


# ErrorDetail : This field is required


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        for key, value in response.data.items():

            for error in value:
                if type(error) is ErrorDetail:  # ErrorDetail or UniqueValidator
                    response.data[key] = error
                    print(response.data)

    return response
