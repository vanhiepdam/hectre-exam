from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.rest_framework.exceptions import BusinessLogicValidationError


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response and (
            isinstance(exc, ValidationError) or isinstance(exc, BusinessLogicValidationError)
    ):
        data = {
            'errors': [
                exc.message
            ],
            'messages': [
                exc.message
            ]
        }
        return Response(data=data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if not response:
        return response
    data = response.data
    str_messages = []
    response.data = {}
    response.data['errors'] = data
    if isinstance(data, list) or isinstance(data, tuple):
        str_messages.extend(data)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) or isinstance(value, tuple):
                str_messages.extend(value)
            else:
                str_messages.append(value)
    else:
        str_messages.append(data)
    response.data['messages'] = str_messages
    return response
