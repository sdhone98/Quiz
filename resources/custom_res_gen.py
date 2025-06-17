from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response


def response_builder(result=None, status_code=status.HTTP_200_OK, message=""):
    if result is None:
        result = []
    return Response(
        {"data": result,
         "status_code": status_code,
         "message": message,
         "time_stamp": now()
         },
        status=status_code
    )