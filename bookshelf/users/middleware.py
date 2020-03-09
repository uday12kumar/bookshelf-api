from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

from bookshelf.users.models import UserToken

ALLOW_WITHOUT_AUTH = ['/api/v1/users/register/', '/api/v1/users/login/']


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.__contains__('api/v1'):
            if not request.path_info in ALLOW_WITHOUT_AUTH:
                try:
                    UserToken.objects.get(key=request.headers['Authorization'])
                except UserToken.DoesNotExist:
                    response = self.get_response(request)
                    return JsonResponse({"message": "Invalid Token"}, status=401)

        response = self.get_response(request)
        return response
