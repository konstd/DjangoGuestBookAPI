from rest_framework.exceptions import NotFound
from rest_framework.exceptions import APIException


def error404(request):
    return NotFound(detail='Error 404, endpoint not found', code=404)


def error500(request):
    return APIException(detail='Error 500, API exception', code=500)
