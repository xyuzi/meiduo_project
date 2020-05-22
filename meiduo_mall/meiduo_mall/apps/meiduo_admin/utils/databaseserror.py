from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.status import HTTP_504_GATEWAY_TIMEOUT
from django.db import DatabaseError


def my_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, DatabaseError):
            response = Response({'err': '数据库无了'}, status=HTTP_504_GATEWAY_TIMEOUT)

    return response
